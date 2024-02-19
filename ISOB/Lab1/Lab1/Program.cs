using Microsoft.VisualBasic.FileIO;
using System;

public class CaesarCipher
{
	const string alfabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

	private string CodeEncode(string text, int k)
	{
		var fullAlfabet = alfabet + alfabet.ToLower();
		var letterQty = fullAlfabet.Length;
		var retVal = "";
		for (int i = 0; i < text.Length; i++)
		{
			var c = text[i];
			var index = fullAlfabet.IndexOf(c);
			if (index < 0)
			{
				retVal += c.ToString();
			}
			else
			{
				var codeIndex = (letterQty + index + k) % letterQty;
				retVal += fullAlfabet[codeIndex];
			}
		}

		return retVal;
	}

	public string Encrypt(string plainMessage, int key)
		=> CodeEncode(plainMessage, key);

	public string Decrypt(string encryptedMessage, int key)
		=> CodeEncode(encryptedMessage, -key);
}

public class VigenereCipher
{
	const string defaultAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
	readonly string letters;

	public VigenereCipher(string alphabet = null)
	{
		letters = string.IsNullOrEmpty(alphabet) ? defaultAlphabet : alphabet;
	}

	private string GetRepeatKey(string s, int n)
	{
		var p = s;
		while (p.Length < n)
		{
			p += p;
		}

		return p.Substring(0, n);
	}

	private string Vigenere(string text, string password, bool encrypting = true)
	{
		var gamma = GetRepeatKey(password, text.Length);
		var retValue = "";
		var q = letters.Length;

		for (int i = 0; i < text.Length; i++)
		{
			var letterIndex = letters.IndexOf(text[i]);
			var codeIndex = letters.IndexOf(gamma[i]);
			if (letterIndex < 0)
			{
				retValue += text[i].ToString();
			}
			else
			{
				retValue += letters[(q + letterIndex + ((encrypting ? 1 : -1) * codeIndex)) % q].ToString();
			}
		}

		return retValue;
	}

	public string Encrypt(string plainMessage, string password)
		=> Vigenere(plainMessage, password);

	public string Decrypt(string encryptedMessage, string password)
		=> Vigenere(encryptedMessage, password, false);
}


class Program
{
	static void Main(string[] args)
	{
		var cipher = new CaesarCipher();
		string? message;
		using (var sr = new StreamReader("../../../File.txt"))
		{
			message = sr.ReadToEnd();
		}
		Console.WriteLine($"Текст из файла: {message}");
		Console.Write("Введите ключ (Цезарь): ");
		var secretKey = Convert.ToInt32(Console.ReadLine());
		var encryptedText = cipher.Encrypt(message, secretKey);
		Console.WriteLine($"Зашифрованное сообщение (Цезарь): {encryptedText}");
		Console.WriteLine($"Расшифрованное сообщение (Цезарь): {cipher.Decrypt(encryptedText, secretKey)}");

		var cipher_V = new VigenereCipher();
		string? inputText;
		using (var sr = new StreamReader("../../../File.txt"))
		{
			inputText = sr.ReadToEnd().ToUpper();
		}
		Console.Write("Введите ключ (Виженер): ");
		var password = Console.ReadLine().ToUpper();
		encryptedText = cipher_V.Encrypt(inputText, password);
		Console.WriteLine($"Зашифрованное сообщение (Виженер): {encryptedText}");
		Console.WriteLine($"Расшифрованное сообщение (Виженер): {cipher_V.Decrypt(encryptedText, password)}");
		Console.ReadLine();
	}
}
