using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Numerics;
using System.Runtime.InteropServices;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace Kerberos;

public static class Des
{
	private static readonly int[] InitialPermutation =
	[
		57, 49, 41, 33, 25, 17, 9,  1, 59, 51, 43, 35, 27, 19, 11, 3,
		61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7,
		56, 48, 40, 32, 24, 16, 8,  0, 58, 50, 42, 34, 26, 18, 10, 2,
		60, 52, 44, 36, 28, 20, 12, 4, 62, 54, 46, 38, 30, 22, 14, 6
	];

	private static readonly int[] InversePermutation =
	[
		39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30,
		37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52, 20, 60, 28,
		35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26,
		33, 1, 41, 9,  49, 17, 57, 25, 32, 0, 40, 8,  48, 16, 56, 24,
	];

	private static readonly int[][] SBoxes =
	[
		[
			14, 4,  13, 1,  2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0,  7,
			0,  15, 7,  4,  14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3,  8,
			4,  1,  14, 8,  13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5,  0,
			15, 12, 8,  2,  4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6,  13
		],
		[
			15, 1,  8,  14, 6,  11, 3,  4,  9,  7,  2,  13, 12, 0,  5,  10,
			3,  13, 4,  7,  15, 2,  8,  14, 12, 0,  1,  10, 6,  9,  11, 5,
			0,  14, 7,  11, 10, 4,  13, 1,  5,  8,  12, 6,  9,  3,  2,  15,
			13, 8,  10, 1,  3,  15, 4,  2,  11, 6,  7,  12, 0,  5,  14, 9
		],
		[
			10, 0,  9,  14, 6,  3,  15, 5,  1,  13, 12, 7,  11, 4,  2,  8,
			13, 7,  0,  9,  3,  4,  6,  10, 2,  8,  5,  14, 12, 11, 15, 1,
			13, 6,  4,  9,  8,  15, 3,  0,  11, 1,  2,  12, 5,  10, 14, 7,
			1,  10, 13, 0,  6,  9,  8,  7,  4,  15, 14, 3,  11, 5,  2,  12
		],
		[
			7,  13, 14, 3,  0,  6,  9,  10, 1,  2,  8,  5,  11, 12, 4,  15,
			13, 8,  11, 5,  6,  15, 0,  3,  4,  7,  2,  12, 1,  10, 14, 9,
			10, 6,  9,  0,  12, 11, 7,  13, 15, 1,  3,  14, 5,  2,  8,  4,
			3,  15, 0,  6,  10, 1,  13, 8,  9,  4,  5,  11, 12, 7,  2,  14
		],
		[
			2,  12, 4,  1,  7,  10, 11, 6,  8,  5,  3,  15, 13, 0,  14, 9,
			14, 11, 2,  12, 4,  7,  13, 1,  5,  0,  15, 10, 3,  9,  8,  6,
			4,  2,  1,  11, 10, 13, 7,  8,  15, 9,  12, 5,  6,  3,  0,  14,
			11, 8,  12, 7,  1,  14, 2,  13, 6,  15, 0,  9,  10, 4,  5,  3
		],
		[
			12, 1,  10, 15, 9,  2,  6,  8,  0,  13, 3,  4,  14, 7,  5,  11,
			10, 15, 4,  2,  7,  12, 9,  5,  6,  1,  13, 14, 0,  11, 3,  8,
			9,  14, 15, 5,  2,  8,  12, 3,  7,  0,  4,  10, 1,  13, 11, 6,
			4,  3,  2,  12, 9,  5,  15, 10, 11, 14, 1,  7,  6,  0,  8,  13
		],
		[
			4,  11,  2, 14, 15, 0,  8,  13, 3,  12, 9,  7,  5,  10, 6,  1,
			13, 0,  11, 7,  4,  9,  1,  10, 14, 3,  5,  12, 2,  15, 8,  6,
			1,  4,  11, 13, 12, 3,  7,  14, 10, 15, 6,  8,  0,  5,  9,  2,
			6,  11, 13, 8,  1,  4,  10, 7,  9,  5,  0,  15, 14, 2,  3,  12
		],
		[
			13, 2,  8,  4,  6,  15, 11, 1,  10, 9,  3,  14, 5,  0,  12, 7,
			1,  15, 13, 8,  10, 3,  7,  4,  12, 5,  6,  11, 0,  14, 9,  2,
			7,  11, 4,  1,  9,  12, 14, 2,  0,  6,  10, 13, 15, 3,  5,  8,
			2,  1,  14, 7,  4,  10, 8,  13, 15, 12, 9,  0,  3,  5,  6,  11
		]
	];


	private static readonly int[] PermutedChoice1 =   // Перестановка ключа
	[
		56, 48, 40, 32, 24, 16, 8,  0,  57, 49, 41, 33, 25, 17,
		9,  1,  58, 50, 42, 34, 26, 18, 10, 2,  59, 51, 43, 35,
		62, 54, 46, 38, 30, 22, 14, 6,  61, 53, 45, 37, 29, 21,
		13, 5,  60, 52, 44, 36, 28, 20, 12, 4,  27, 19, 11, 3
	];



	private static readonly int[] Rotates =
	[
		1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
	];


	private static readonly int[] PermutedChoice2 =   // Перестановка со сжатием
	[
		13, 16, 10, 23, 0,  4,  2,  27, 14, 5,  20, 9,
		22, 18, 11, 3,  25, 7,  15, 6,  26, 19, 12, 1,
		40, 51, 30, 36, 46, 54, 29, 39, 50, 44, 32, 47,
		43, 48, 38, 55, 33, 52, 45, 41, 49, 35, 28, 31
	];


	private static readonly int[] Expansion =
	[
		31, 0,  1,  2,  3,  4,  3,  4,  5,  6,  7,  8,
		7,  8,  9,  10, 11, 12, 11, 12, 13, 14, 15, 16,
		15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24,
		23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0
	];


	private static readonly int[] Permutation =
	[
		15, 6, 19, 20, 28, 11, 27, 16,
		0, 14, 22, 25, 4, 17, 30, 9,
		1, 7, 23, 13, 31, 26, 2, 8,
		18, 12, 29, 5, 21, 10, 3, 24
	];



	private static IEnumerable<string> SliceMes(string str)
	{
		ArgumentException
			.ThrowIfNullOrWhiteSpace(str, nameof(str));

		int chunkSize = 8;

		for (int i = 0; i < str.Length; i += chunkSize)
		{
			string chunk = str.Substring(i, Math.Min(chunkSize, str.Length - i));
			chunk = chunk.PadLeft(chunkSize, '\0');

			byte[] bytes = Encoding.UTF8.GetBytes(chunk);

			yield return Convert.ToHexString(bytes);
		}
	}

	private static string ToBin(string hexString)
	{
		return string.Join(string.Empty, hexString.Select(c =>
		{
			return Convert.ToString(Convert.ToInt32(c.ToString(), 16), 2).PadLeft(4, '0');
		}));
	}


	private static string Permute(string block, IEnumerable<int> box)
	{
		return string.Join(string.Empty, box.Select(i => block[i]));
	}

	private static string RotateLeft(int block, int i)
	{
		return Convert.ToString((block << i & 0x0fffffff) | (block >> (28 - i)), 2).PadLeft(28, '0');
	}


	private static IEnumerable<string> KeyGen(string block1, string block2)
	{
		foreach (var i in Rotates)   // раунды
		{
			block1 = RotateLeft(Convert.ToInt32(block1, 2), i);
			block2 = RotateLeft(Convert.ToInt32(block2, 2), i);

			yield return Permute(block1 + block2, PermutedChoice2);
		}
	}

	private static string Xor(string arg_1, string arg_2)
	{
		return string.Join(string.Empty, arg_1.Zip(arg_2).Select((lr) => (lr.First ^ lr.Second).ToString()));
	}

	private static string F(string block, string key)
	{
		List<string> final = [];

		var l = Xor(Permute(block, Expansion), key);

		List<string> list = [];

		for (int i = 0; i < l.Length; i += 6)
		{
			list.Add(l.Substring(i, Math.Min(6, l.Length - i)));
		}

		foreach (var (i, j) in list.Select((item, index) => (item, index)))
		{
			int[][] tempBox =
			[
				SBoxes[j][0..16],
				SBoxes[j][16..32],
				SBoxes[j][32..48],
				SBoxes[j][48..64]
			];

			final.Add(Convert.ToString(tempBox[Convert.ToInt32(i[0].ToString() + i[^1], 2)][Convert.ToUInt32(i[1..^1], 2)], 2).PadLeft(4, '0'));
		}


		return Permute(string.Join(string.Empty, final), Permutation);
	}



	private static IEnumerable<string> Des_(string block, IEnumerable<string> keyArray)
	{
		int keyCenter = block.Length / 2;

		string L = block[..keyCenter];
		string R = block[keyCenter..];

		foreach (var i in keyArray)
		{
			(R, L) = (Xor(F(R, i), L), R);
		}

		var l = Permute(R + L, InversePermutation);

		for (int i = 0; i < l.Length; i += 8)
		{
			yield return l.Substring(i, Math.Min(8, l.Length - i));
		}
	}


	private static IEnumerable<string> Cut(this string @string, int length)
	{
		for (int i = 0; i < @string.Length; i += length)
		{
			yield return @string.Substring(i, Math.Min(length, @string.Length - i));
		}
	}


	public static string Encrypt(string data, string key)
	{
		StringBuilder ans = new StringBuilder();

		foreach (var i in SliceMes(data))
		{
			string binMess = ToBin(i);
			string binKey = ToBin(key);

			string permutedBlock = Permute(binMess, InitialPermutation);             // Начальная перестановка
			string permutedKey = Permute(binKey, PermutedChoice1);                  // Начальная перестановка ключа. В итоге преобразуется в 56 бит.


			int keyCenter = permutedKey.Length / 2;

			string L = permutedKey[..keyCenter];
			string R = permutedKey[keyCenter..];

			List<string> keyList = KeyGen(L, R).ToList();

			var l = Des_(permutedBlock, keyList).Select(i => Convert.ToString(Convert.ToInt32(i, 2), 16).PadLeft(2, '0').ToUpper());

			ans.Append(string.Join(string.Empty, l));
		}

		return ans.ToString();
	}

	public static string Decrypt(string data, string key)
	{
		List<string> ans = [];

		foreach (var i in data.Cut(16))
		{
			string binMess = ToBin(i);
			string binKey = ToBin(key);


			string permutedBlock = Permute(binMess, InitialPermutation);
			string permutedKey = Permute(binKey, PermutedChoice1);


			int keyCenter = permutedKey.Length / 2;

			string L = permutedKey[..keyCenter];
			string R = permutedKey[keyCenter..];

			List<string> keyList = KeyGen(L, R).ToList();


			var l = Des_(permutedBlock, keyList.AsEnumerable().Reverse()).Select(i => Convert.ToString(Convert.ToInt32(i, 2), 16).PadLeft(2, '0').ToUpper());

			ans.Add(string.Join(string.Empty, l));
		}


		return string.Join(string.Empty, ans.Select(s => new string(s.Cut(2).Select(c => Convert.ToInt32(c, 16)).Where(i => i != 0).Select(i => (char)i).ToArray())));
	}

	public static string CreateRandomKey()
	{
		char[] array = new char[16];

		for (int i = 0; i < array.Length; i++)
		{
			array[i] = "1234567890ABCDEF"[Random.Shared.Next(array.Length)];
		}

		return new string(array);
	}
}
