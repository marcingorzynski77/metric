using System;
using System.Collections.Generic;
using System.Text;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System.Threading;

namespace Client
{
    public class RabbitSender : IDisposable
    {
        private const string HostName = "localhost";
        private const string UserName = "guest";
        private const string Password = "guest";
        private const bool IsDurable = false;
        private const string ExchangeName = "Module2.Sample8.Exchange";
        //The two below settings are just to illustrate how they can be used but we are not using them in
        //this sample as we will use the defaults
        private const string VirtualHost = "";
        private int Port = 0;

        private string _responseQueue;
        private ConnectionFactory _connectionFactory;
        private IConnection _connection;
        private IModel _model;
        private QueueingBasicConsumer _consumer;

        /// <summary>
        /// Ctor
        /// </summary>
        public RabbitSender()
        {
            DisplaySettings();
            SetupRabbitMq();
        }

        private void DisplaySettings()
        {
            Console.WriteLine("Host: {0}", HostName);
            Console.WriteLine("Username: {0}", UserName);
            Console.WriteLine("Password: {0}", Password);
            Console.WriteLine("VirtualHost: {0}", VirtualHost);
            Console.WriteLine("Port: {0}", Port);
            Console.WriteLine("Is Durable: {0}", IsDurable);
        }
        /// <summary>
        /// Sets up the connections for rabbitMQ
        /// </summary>
        private void SetupRabbitMq()
        {
            _connectionFactory = new ConnectionFactory
            {
                HostName = HostName,
                UserName = UserName,
                Password = Password
            };

            if (string.IsNullOrEmpty(VirtualHost) == false)
                _connectionFactory.VirtualHost = VirtualHost;
            if (Port > 0)
                _connectionFactory.Port = Port;

            _connection = _connectionFactory.CreateConnection();
            _model = _connection.CreateModel();

            _responseQueue = _model.QueueDeclare().QueueName;
            _consumer = new QueueingBasicConsumer(_model);
            _model.BasicConsume(_responseQueue, true, _consumer);
        }

        public List<string> Send(string message, string routingKey, TimeSpan timeout, int minResponses)
        {
            var responses = new List<string>();
            var correlationToken = Guid.NewGuid().ToString();

            //Setup properties
            var properties = _model.CreateBasicProperties();
            properties.ReplyTo = _responseQueue;
            properties.CorrelationId = correlationToken;

            //Serialize
            byte[] messageBuffer = Encoding.Default.GetBytes(message);

            //Send
            var timeoutAt = DateTime.Now + timeout;
            _model.BasicPublish(ExchangeName, routingKey, properties, messageBuffer);

            //Wait for response
            while (DateTime.Now <= timeoutAt)
            {
                object result = null;
                _consumer.Queue.Dequeue(10, out result);
                if (result == null)
                {
                    //No more messages on queue at present so if we have already got the minimum expected responses then
                    //lets just return those
                    if (responses.Count >= minResponses)
                        return responses;

                    Console.WriteLine("Waiting for responses");
                    Thread.Sleep(new TimeSpan(0, 0, 0, 0, 200));
                    continue;
                }

                var deliveryArgs = (BasicDeliverEventArgs)result;
                if (deliveryArgs.BasicProperties == null ||
                    deliveryArgs.BasicProperties.CorrelationId != correlationToken) continue;

                var response = Encoding.Default.GetString(deliveryArgs.Body);
                Console.WriteLine("Sender got response: {0}", response);
                responses.Add(response);
                
            }
            return responses;
        }

        /// <summary>
        /// Dispose
        /// </summary>
        public void Dispose()
        {
            if (_connection != null)
                _connection.Close();
            
            if (_model != null && _model.IsOpen)
                _model.Abort();

            _connectionFactory = null;

            GC.SuppressFinalize(this);
        }
    }
}
