#pragma once
#ifndef DELTA
#define DELTA
#include"Vector3.h"
//using namespace std;
class Delta {
public:
	Delta();
	Delta(double dx, double dy, double dz, double dvx, double dvy, double dvz);
	Vector3 deltav;
	Vector3 deltap;
	Delta operator+(Delta d2);
	Delta operator-(Delta d2);
	Delta operator*(double num);
	Delta operator/(double num);
};

#endif