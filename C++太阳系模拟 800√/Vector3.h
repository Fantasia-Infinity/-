#pragma once
#ifndef VECTOR3
#define VECTOR3

class Vector3 {
public:
	double x;
	double y;
	double z;
	Vector3(double x, double y, double z);
	void init(double x, double y, double z);
	Vector3();
	Vector3 operator+(Vector3 v2);
	Vector3 operator-(Vector3 v2);
	Vector3 operator*(double num);
	Vector3 operator/(double num);
};

#endif 