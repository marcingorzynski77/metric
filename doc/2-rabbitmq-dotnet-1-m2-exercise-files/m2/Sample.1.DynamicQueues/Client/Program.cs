using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using RabbitMQ.Client;

namespace Client
{
    class Program
    {
        private const string HostName = "localhost";
        private const string UserName = "guest";
        private const string Password = "guest";
        

        private static void Main(string[] args)
        {
            Console.WriteLine("Starting RabbitMQ Queue Creator");
            Console.WriteLine();
            Console.WriteLine();

            var connectionFactory = new ConnectionFactory
            {
                HostName = HostName,
                UserName = UserName,
                Password = Password
            };

            var connection = connectionFactory.CreateConnection();
            var model = connection.CreateModel();

            model.QueueDeclare("MyQueue", true, false, false, null);
            Console.WriteLine("Queue created");

            model.ExchangeDeclare("MyExchange", ExchangeType.Topic);
            Console.WriteLine("Exchange created");

            model.QueueBind("MyQueue", "MyExchange", "cars");
            Console.WriteLine("Exchange and queue bound");

            Console.ReadLine();
        }
    }
}
