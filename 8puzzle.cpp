#include <stdio.h>
#include <queue>
#include <iostream>
#include <algorithm>
#include <vector>
#include <time.h>
#include <Windows.h>

using namespace std;
#define N 3 

struct Node
{
	Node* parent;
	Node* child[4];
	int mat[N][N];
	int x, y;
	int cost;
	int level;
	bool search;
};

void printMatrix(int mat[N][N])
{
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
			printf("%d ", mat[i][j]);
		printf("\n");
	}
}

// Function to allocate a new node 
Node* newNode(int mat[N][N], int x, int y, int newX, int newY, int level, Node* parent)
{
	Node* node = new Node;

	node->parent = parent;

	for (int i = 0; i < 4; i++)
		node->child[i] = NULL;

	memcpy(node->mat, mat, sizeof(node->mat));

	swap(node->mat[x][y], node->mat[newX][newY]);
 
	node->cost = INT_MAX;
 
	node->level = level;
	node->search = false;
	node->x = newX;
	node->y = newY;

	return node;
}

int row[] = { 1, 0, -1, 0 };
int col[] = { 0, -1, 0, 1 };

int calculateCost(int initial[N][N], int final[N][N])
{
	int count = 0;
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
			if (initial[i][j] && initial[i][j] != final[i][j])
				count += (abs((initial[i][j]-1) / N - i) + abs((initial[i][j]-1) % N - j));
	return count;
}

int isSafe(int x, int y)
{
	return (x >= 0 && x < N && y >= 0 && y < N);
}

void printPath(Node* root)
{
	if (root == NULL)
		return;

	printPath(root->parent);

	while (cin.get() != '\n')
		Sleep(100);

	printMatrix(root->mat);
	printf("\n");
}

struct comp
{
	bool operator()(const Node* lhs, const Node* rhs) const
	{
		return (lhs->cost + lhs->level) > (rhs->cost + rhs->level);
	}
};

Node *root;
priority_queue<Node*, std::vector<Node*>, comp> g_pq;
int final[N][N] = { { 1, 2, 3 },{ 4, 5, 6 },{ 7, 8, 0 } };

bool DST(Node* node, int threshold)
{
	if (node == NULL) return false;

	if (node->cost == 0) {
		printf("Find Solution:\n");
		printPath(node);
		return true;
	}

	if (node->cost + node->level > threshold) {
		g_pq.push(node);
		return false;
	}

	node->search = true;

	for (int i = 0; i < 4; i++) {
		if (isSafe(node->x + row[i], node->y + col[i])) {
			Node* child = newNode(node->mat, node->x, node->y, node->x + row[i], node->y + col[i], node->level + 1, node);
			child->cost = calculateCost(child->mat, final);

			node->child[i] = child;
			if (DST(node->child[i], threshold)) return true;

		}
	}
	return false;
}

bool solve(int initial[N][N], int x, int y, int final[N][N], int threshold)
{
	priority_queue<Node*, std::vector<Node*>, comp> pq(g_pq);
	g_pq = priority_queue<Node*, std::vector<Node*>, comp> ();
 
	while (!pq.empty())
	{
		Node* min = pq.top();
		pq.pop();

		if (DST(min, threshold))
			return true;

	}

	return false;
}

int main()
{ 
	int initial[N][N] = { { 5, 1, 0 },
	{ 7, 4, 8 },
	{ 6, 3, 2 } };
	int x = 0, y = 2, threshold = 0;
	vector<int> arr;
	
	for (int i = 0; i < N*N; i++)
		arr.push_back(i);

	srand(time(0));
	random_shuffle(arr.begin(), arr.end());

	printf("Initial Puzzle:\n");
	for (int i = 0; i < N*N; i++) {
		initial[i / N][i % N] = arr[i];
		if (arr[i] == 0) {
			x = i / N;
			y = i % N;
			printf("%d  %d \n", x, y);
		}
	}
	printMatrix(initial);

	root = newNode(initial, x, y, x, y, 0, NULL);
	root->cost = calculateCost(initial, final);
	g_pq.push(root);
	
	while (!solve(initial, x, y, final, threshold)) {
		threshold += 1;
		printf("Next level: %d\n", threshold);/*
		printf("pd %d\n", g_pq.size());
		while (cin.get() != '\n')
			Sleep(100);*/
	}

	while (cin.get() != '\n')
		Sleep(100);

	return 0;
}