#include <stdio.h>
#include <queue>
#include <iostream>
#include <algorithm>
#include <vector>
#include <time.h>
#include <Windows.h>
using namespace std;
#define N 4 

struct Node
{ 
	Node* parent; 
	int dir;
	int x, y;
	int cost;
	int level;
};
 
void printMatrix(int mat[N][N])
{
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
			printf("%2d ", mat[i][j]);
		printf("\n");
	}
}

Node* newNode(int newX, int newY, int level, Node* parent, int dir)
{
	Node* node = new Node;

	node->parent = parent;
	node->cost = INT_MAX;
	node->level = level;
	node->x = newX;
	node->y = newY;
	node->dir = dir;

	return node;
}

class MinHeap {
	public:
		static vector<Node*> heap;

		static bool min_comp(int a, int b) {
			return (heap[a]->cost + heap[a]->level > heap[b]->cost + heap[b]->level);
		}

		static void add(Node* node) {
			heap.push_back(node);
			int index = heap.size() - 1;
			while (index >= 0) {
				int parent_index = (index - 1) / 2;
				if (min_comp(parent_index, index)) {
					Node* temp = heap[parent_index];
					heap[parent_index] = heap[index];
					heap[index] = temp;

					index = parent_index;
				}
				else
					break;
			}
		}

		static Node* get_min() {
			if (heap.size() == 0)
				return NULL;

			Node* min = heap[0];
			int index = 0, size = heap.size();
			heap[index] = heap[size - 1];
			heap.pop_back();
			size--;

			while (index < size) {
				int min_index = index;

				if (min(min_index, index + 1))
					min_index = index + 1;
				if (min(min_index, index + 2))
					min_index = index + 2;

				if (index != min_index) {
					Node* temp = heap[index];
					heap[index] = heap[min_index];
					heap[min_index] = temp;

					index = min_index;
				}
				else
					break;
			}

			return min;
		}
};

int row[] = { 1, 0, -1, 0 };
int col[] = { 0, -1, 0, 1 };

int final[N][N] = { { 1, 2, 3, 4 },{ 5, 6, 7, 8 },{ 9, 10, 11, 12 },{ 13, 14, 15, 0 } };

int initial[N][N] = { { 11,4,12,2 },{ 5,10,3,15 },{ 14,1,6,7 },{ 0,9,8,13 } };
//int initial[N][N] = { { 5,2,4,8 },{ 10,0,3,14 },{ 13,6,11,12 },{ 1,15,9,7 } };

vector<Node*> MinHeap::heap;
vector<Node*> q;

void getMat(Node* node, int* ans) {
	if (node->parent == NULL) {
		memcpy(ans, initial, sizeof initial);
		return;
	}
	//printf("x:%d, y:%d\n", node->parent->x + row[node->dir], node->parent->y + col[node->dir]);
	getMat(node->parent, ans);
	swap(*(ans+node->x*N + node->y), *(ans+node->parent->x*N + node->parent->y));
}

void debug(Node* min) {
	printf("Level:%d, Cost:%d\n", min->level, min->cost);
	int mat[N][N];
	getMat(min, &mat[0][0]);
	printMatrix(mat);
	while (cin.get() != '\n')
		Sleep(100);
}

int calculateCost(int initial[N][N], int final[N][N])
{
	
	int count = 0;
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++) {
			if (initial[i][j] && initial[i][j] != final[i][j])
				count += (abs((initial[i][j] - 1) / N - i) + abs((initial[i][j] - 1) % N - j));
		}

	count *= 1.2;

	return count;
}

int isSafe(int x, int y)
{
	return (x >= 0 && x < N && y >= 0 && y < N);
}

bool solvable(int mat[N][N]) {
	int count = 0;
	for (int i = 0; i < N*N; i++) {
		for (int j = i + 1; j < N*N; j++) {
			if (mat[i / N][i%N] && mat[i / N][i%N] > mat[j / N][j%N] && mat[j / N][j%N] != 0)
				count++;
			else if (mat[i / N][i%N] == 0) {
				count += N - i / N;
				break;
			}
		}
	}

	if (mat[3][3] == 0)
		count += 1;

	if (count % 2 != 0) {
		printf("solve:%d\n", count);
		return true;
	}

	return false;
}

void printPath(Node* root)
{
	if (root == NULL)
		return;

	printPath(root->parent);

	while (cin.get() != '\n')
		Sleep(100);

	int mat[N][N];
	getMat(root, &mat[0][0]);
	printMatrix(mat);
	printf("\n");
}

bool solve(int threshold)
{ 
	for (auto i = q.begin(); i != q.end(); i++)
		MinHeap::add(*i);

	q.clear();

	while (MinHeap::heap.size() != 0)
	{
		Node* min = MinHeap::get_min();

		if (min->level + min->cost > threshold) {
			q.push_back(min);
			continue;
		}

		if (min->cost == 0)
		{
			printf("Find Solution:%d Steps\n", min->level);
			printPath(min);
			return true;
		}

		int mat[N][N];
		getMat(min, &mat[0][0]);

		for (int i = 0; i < 4; i++)
		{
			Node* parent = min->parent;

			if (isSafe(min->x + row[i], min->y + col[i]) && (parent->x != min->x + row[i] || parent->y != min->y + col[i]))
			{
				Node* child = newNode(min->x + row[i], min->y + col[i], min->level + 1, min, i);

				swap(mat[min->x][min->y], mat[min->x + row[i]][min->y + col[i]]);
				child->cost = calculateCost(mat, final);
				swap(mat[min->x + row[i]][min->y + col[i]], mat[min->x][min->y]);

				MinHeap::add(child);
				//printf("Choose:%d\n", min->level);
				//debug(child);
			}
		}
	}

	return false;
}
 
int main()
{
	int x = 3, y = 0, threshold = 30;
	vector<int> arr;
	
	while (true) {
		for (int i = 0; i < N*N; i++)
			arr.push_back(i);

		srand(time(0));
		random_shuffle(arr.begin(), arr.end());

		for (int i = 0; i < N*N; i++) {
			initial[i / N][i % N] = arr[i];
			if (arr[i] == 0) {
				x = i / N;
				y = i % N;
			}
		}

		if (solvable(initial))
			break;

		arr.clear();
	}

	printf("Initial Puzzle:\n");
	printMatrix(initial);

	Node* min = newNode(x, y, 0, NULL, -1);
	min->cost = calculateCost(initial, final);

	int mat[N][N];
	memcpy(mat, initial, sizeof mat);

	for (int i = 0; i < 4; i++)
	{	
		if (isSafe(min->x + row[i], min->y + col[i]))
		{
			Node* child = newNode(min->x + row[i], min->y + col[i], min->level + 1, min, i);

			swap(mat[min->x][min->y], mat[min->x + row[i]][min->y + col[i]]);
			child->cost = calculateCost(mat, final);
			swap(mat[min->x + row[i]][min->y + col[i]], mat[min->x][min->y]);

			MinHeap::add(child);
			//printf("%d..\n", i);
			//debug(child);
		}
	}

	
	while (!solve(threshold)) {
		threshold += 10;
		printf("Threshold:%d\n", threshold);
	}


	while (cin.get() != '\n')
		Sleep(100);

	return 0;
}