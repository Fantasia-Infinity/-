#include "Vector3.h"
Vector3::Vector3(double x, double y, double z){
	this->x = x;
	this->y = y;
	this->z = z;
}

void Vector3::init(double x, double y, double z){
	this->x = x;
	this->y = y;
	this->z = z;
}

Vector3::Vector3() {
}

Vector3 Vector3::operator+(Vector3 v2){
	Vector3 v =Vector3();
	v.x = this->x + v2.x;
	v.y = this->y + v2.y;
	v.z = this->z + v2.z;
	return v;
}

Vector3 Vector3::operator-(Vector3 v2){
	Vector3 v = Vector3();
	v.x = this->x - v2.x;
	v.y = this->y - v2.y;
	v.z = this->z - v2.z;
	return v;
}

Vector3 Vector3::operator*(double num){
	Vector3 v =Vector3();
	v.x = this->x * num;
	v.y = this->y * num;
	v.z = this->z * num;
	return v;
}

Vector3 Vector3::operator/(double num){
	Vector3 v = Vector3();
	v.x = this->x / num;
	v.y = this->y / num;
	v.z = this->z / num;
	return v;
}
