using Kerberos;


public class Program
{
	private static void Main(string[] args)
	{
		var client1 = new Client(Des.CreateRandomKey());
		var client2 = new Client(Des.CreateRandomKey());
		var client3 = new Client(Des.CreateRandomKey());

		var server1 = servers.Single(s => s.Identifier == "server1");
		var server2 = servers.Single(s => s.Identifier == "server2");

		Kdc.AddClient(client1);
		Kdc.AddClient(client2);

		Console.WriteLine(client1.GetData(server1));
		Console.WriteLine(client1.GetData(server1));

		Thread.Sleep(TimeSpan.FromSeconds(16));

		Console.WriteLine(client1.GetData(server1));
	}


	public class Client
	{
		internal string _identifier;

		private string? _encryptedTgt;
		private string? _tgsClientKey;

		private Dictionary<string, string> _servers;


		public Client(string identifier)
		{
			_identifier = identifier;
			_servers = [];
		}


		public string GetData(Server server)
		{
			if (!_servers.ContainsKey(server.Identifier))
				ConnectToServer(server);

			try
			{
				return server.GetData(_identifier, _servers[server.Identifier]);
			}
			catch (InvalidOperationException)
			{
				ConnectToServer(server);
				return server.GetData(_identifier, _servers[server.Identifier]);
			}
		}


		private void ConnectToServer(Server server)
		{
			if (_encryptedTgt is null)
			{
				(_encryptedTgt, _tgsClientKey) = GetTgtWithKey();
			}

			string encryptedTgs;
			string clientServerKey;

			try
			{
				(encryptedTgs, clientServerKey) = GetServerKey(server.Identifier, _encryptedTgt, _tgsClientKey!);
			}
			catch (InvalidOperationException)
			{
				(_encryptedTgt, _tgsClientKey) = GetTgtWithKey();
				(encryptedTgs, clientServerKey) = GetServerKey(server.Identifier, _encryptedTgt, _tgsClientKey!);
			}

			CreateServerSession(server, encryptedTgs, clientServerKey);

			_servers[server.Identifier] = clientServerKey;
		}


		private (string, string) GetTgtWithKey()
		{
			Console.WriteLine("\nStep1 - Client send his identifier\n");

			string sessionKeys = Kdc.As.GetSessionKeys(_identifier);

			string decryptedSessionKeys = Des.Decrypt(sessionKeys, _identifier);

			var encryptedTgt = decryptedSessionKeys.Split('|')[0];
			var tgsClientKey = decryptedSessionKeys.Split('|')[1];

			Console.WriteLine($"Step2 - Client get \n encrypted tgt: {encryptedTgt} and \n tgsClientKey: {tgsClientKey}\n");

			return (encryptedTgt, tgsClientKey);
		}

		private (string, string) GetServerKey(string serverId, string encryptedTgt, string tgsClientKey)
		{
			string aut1 = $"{_identifier}|{DateTime.Now}";

			string messageToTgs = $"{encryptedTgt}|{Des.Encrypt(aut1, tgsClientKey)}|{serverId}";


			string keyWithTicket = Kdc.Tgs.GetServerKey(messageToTgs);

			Console.WriteLine($"Step3 - Client send \n serverId: {serverId}, \n encryptedTgt: {encryptedTgt} and \n tgsClientKey: {tgsClientKey}\n");

			var encryptedTgsWithServeKey = Des.Decrypt(keyWithTicket, tgsClientKey);

			var encryptedTgs = encryptedTgsWithServeKey.Split('|')[0];
			var serverKey = encryptedTgsWithServeKey.Split('|')[1];

			Console.WriteLine($"Step4 - Client get \n encryptedTgs: {encryptedTgs} and \n serverKey: {serverKey}\n");

			return (encryptedTgs, serverKey);
		}

		private void CreateServerSession(Server server, string encryptedTgs, string clientServerKey)
		{
			Console.WriteLine($"Step5 - Client send \n encryptedTgs: {encryptedTgs} and \n clientServerKey: {clientServerKey}\n");

			DateTime t4 = DateTime.Now;
			t4 = DateTime.Parse(t4.ToString());


			string aut2 = $"{_identifier}|{t4}";

			string encryptedTimeToCheck = server.CreateSession($"{encryptedTgs}|{Des.Encrypt(aut2, clientServerKey)}");


			DateTime timeToCheck;

			try
			{
				timeToCheck = DateTime.Parse(Des.Decrypt(encryptedTimeToCheck, clientServerKey));
			}
			catch (FormatException ex)
			{
				throw new InvalidOperationException("Invalid datetime format.", ex);
			}


			if (timeToCheck - TimeSpan.FromSeconds(1) != t4)
				throw new InvalidOperationException("Incorrect response from the server.");

			Console.WriteLine("Step6 - Client connected with server\n");
		}
	}


	public static class Kdc
	{
		private static HashSet<string> _clients;


		static Kdc()
		{
			_clients = [];
		}


		public static void AddClient(Client client) => _clients.Add(client._identifier);

		public static class As
		{
			public static string GetSessionKeys(string clientIdentifier)
			{
				if (!_clients.Contains(clientIdentifier))
					throw new ArgumentException("Client with this identifier is not registered in this server.");

				var tgsId = Tgs._id;
				var tgsKey = Tgs._key;


				var tgsClientKey = Des.CreateRandomKey(); //Random.Shared.Next(100).ToString();

				string tgt = $"{clientIdentifier}|{tgsId}|{DateTime.Now}|{TimeSpan.FromSeconds(15)}|{tgsClientKey}";

				return Des.Encrypt(Des.Encrypt(tgt, tgsKey) + '|' + tgsClientKey, clientIdentifier);
			}
		}

		public static class Tgs
		{
			internal static string _id;
			internal static string _key;

			static Tgs()
			{
				_id = "123";
				_key = Des.CreateRandomKey();
			}


			public static string GetServerKey(string message)
			{
				string encryptedTgt;
				string encryptedAut1;
				string serverId;

				try
				{
					encryptedTgt = message.Split('|')[0];
					encryptedAut1 = message.Split('|')[1];
					serverId = message.Split('|')[2];
				}
				catch (IndexOutOfRangeException e)
				{
					throw new InvalidOperationException("Invalid format of message.", e);
				}

				string serverKey;

				

				try
				{
					serverKey = servers.Where(s => s.Identifier == serverId).Single().Key;
				}
				catch (InvalidOperationException e)
				{
					throw new InvalidOperationException("Invalid server id.", e);
				}


				string tgt;

				try
				{
					tgt = Des.Decrypt(encryptedTgt, _key);
				}
				catch (InvalidOperationException e)
				{
					throw new InvalidOperationException("Can't decrypt TGT.", e);
				}

				string clientId;
				string tgsId;
				string t1;
				string p1;
				string clientTgsKey;

				try
				{
					clientId = tgt.Split('|')[0];
					tgsId = tgt.Split('|')[1];
					t1 = tgt.Split('|')[2];
					p1 = tgt.Split('|')[3];
					clientTgsKey = tgt.Split('|')[4];
				}
				catch (IndexOutOfRangeException e)
				{
					throw new InvalidOperationException("Invalid format of TGT.", e);
				}

				if (tgsId != _id)
					throw new InvalidOperationException("Invalid tgs id.");

				string aut1;

				try
				{
					aut1 = Des.Decrypt(encryptedAut1, clientTgsKey);
				}
				catch (InvalidOperationException e)
				{
					throw new InvalidOperationException("Can't decrypt TGT.", e);
				}

				string clientId2;
				string t2;

				try
				{
					clientId2 = aut1.Split('|')[0];
					t2 = aut1.Split('|')[1];
				}
				catch (IndexOutOfRangeException e)
				{
					throw new InvalidOperationException("Invalid format of Aut1.", e);
				}

				if (clientId != clientId2)
					throw new InvalidOperationException("The client who requested access to the server is not the one who requested the ticket.");

				try
				{
					if (DateTime.Parse(t1) + TimeSpan.Parse(p1) < DateTime.Parse(t2))
						throw new InvalidOperationException("The mandate has expired.");
				}
				catch (FormatException ex)
				{
					throw new InvalidOperationException("Invalid datetime format.", ex);
				}

				string clientServerKey = Des.CreateRandomKey(); //Random.Shared.NextSingle().ToString();

				string tgs = $"{clientId}|{serverId}|{DateTime.Now}|{TimeSpan.FromSeconds(15)}|{clientServerKey}";

				return Des.Encrypt($"{Des.Encrypt(tgs, serverKey)}|{clientServerKey}", clientTgsKey);
			}
		}
	}


	static List<Server> servers =
	[
		new("server1", Des.CreateRandomKey()),
		new("server2", Des.CreateRandomKey())
	];

	public class Server
	{
		public string Identifier { get; init; }
		internal string Key { get; init; }

		private Dictionary<string, string> _clients = [];


		public Server(string identifier, string key)
		{
			Identifier = identifier;
			Key = key;
		}


		public string CreateSession(string message)
		{
			string encryptedTgs;
			string encryptedAut2;

			try
			{
				encryptedTgs = message.Split('|')[0];
				encryptedAut2 = message.Split('|')[1];
			}
			catch (IndexOutOfRangeException e)
			{
				throw new InvalidOperationException("Invalid format of message.", e);
			}

			string tgs;

			try
			{
				tgs = Des.Decrypt(encryptedTgs, Key);
			}
			catch (InvalidOperationException e)
			{
				throw new InvalidOperationException("Can't decrypt TGS.", e);
			}

			string clientId;
			string serverId;
			string t3;
			string p2;
			string clientServerKey;

			try
			{
				clientId = tgs.Split('|')[0];
				serverId = tgs.Split('|')[1];
				t3 = tgs.Split('|')[2];
				p2 = tgs.Split('|')[3];
				clientServerKey = tgs.Split('|')[4];
			}
			catch (IndexOutOfRangeException e)
			{
				throw new InvalidOperationException("Invalid format of TGS.", e);
			}

			if (serverId != Identifier)
				throw new InvalidOperationException("Tgs server id not equal with this server id.");

			string aut2;

			try
			{
				aut2 = Des.Decrypt(encryptedAut2, clientServerKey);
			}
			catch (InvalidOperationException e)
			{
				throw new InvalidOperationException("Can't decrypt aut2.", e);
			}

			string clientId2;
			string t4;

			try
			{
				clientId2 = aut2.Split('|')[0];
				t4 = aut2.Split('|')[1];
			}
			catch (IndexOutOfRangeException e)
			{
				throw new InvalidOperationException("Invalid format of Aut1.", e);
			}

			if (clientId != clientId2)
				throw new InvalidOperationException("Client id in tgs not equal to client id in aut block.");

			try
			{
				if (DateTime.Parse(t3) + TimeSpan.Parse(p2) < DateTime.Parse(t4))
					throw new InvalidOperationException("The tgs has expired.");
			}
			catch (FormatException ex)
			{
				throw new InvalidOperationException("Invalid datetime format.", ex);
			}

			_clients[clientId] = clientServerKey;

			Task.Delay(DateTime.Parse(t3) + TimeSpan.Parse(p2) - DateTime.Now).ContinueWith(t =>
			{
				_clients.Remove(clientId);
			});

			string timeToCheck = (DateTime.Parse(t4) + TimeSpan.FromSeconds(1)).ToString();
			return Des.Encrypt(timeToCheck, clientServerKey);
		}

		public string GetData(string clientId, string clientServerKey)
		{
			if (!_clients.TryGetValue(clientId, out var clientServerKey2))
				throw new InvalidOperationException("This client not registered on server.");

			if (clientServerKey != clientServerKey2)
				throw new InvalidOperationException("Invalid server key.");



			return "Client get data from server";
		}
	}
}
