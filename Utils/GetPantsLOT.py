def GetPantsLOT(Color):  # Get color assigned to IDs in the CDClient
	lot = -1
	lots = {0: 2508, 1: 2519, 3: 2515, 5: 2509, 6: 2524, 7: 2521, 8: 2522, 9: 2526, 10: 2523, 11: 2513, 13: 2527,
			14: 2517, 15: 2516, 16: 2511, 84: 2520, 96: 2514}

	return lots[Color]
