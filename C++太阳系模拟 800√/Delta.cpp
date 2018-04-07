#include "Delta.h"


Delta::Delta()
{
}

Delta::Delta(double dx, double dy, double dz, double dvx, double dvy, double dvz){
	this->deltap.x = dx;
	this->deltap.y = dy;
	this->deltap.z = dz;
	this->deltav.x = dvx;
	this->deltav.y = dvy;
	this->deltav.z = dvz;
}

Delta Delta::operator+(Delta d2)
{
	Delta d = Delta();
	d.deltap.x = this->deltap.x + d2.deltap.x;
	d.deltap.y = this->deltap.y + d2.deltap.y;
	d.deltap.z = this->deltap.z + d2.deltap.z;
	d.deltav.x = this->deltav.x + d2.deltav.x;
	d.deltav.y = this->deltav.y + d2.deltav.y;
	d.deltav.z = this->deltav.z + d2.deltav.z;
	return d;
}

Delta Delta::operator-(Delta d2)
{
	Delta d = Delta();
	d.deltap.x = this->deltap.x - d2.deltap.x;
	d.deltap.y = this->deltap.y - d2.deltap.y;
	d.deltap.z = this->deltap.z - d2.deltap.z;
	d.deltav.x = this->deltav.x - d2.deltav.x;
	d.deltav.y = this->deltav.y - d2.deltav.y;
	d.deltav.z = this->deltav.z - d2.deltav.z;
	return d;
}

Delta Delta::operator*(double num)
{
	Delta d =Delta();
	d.deltap.x = this->deltap.x*num;
	d.deltap.y = this->deltap.y*num;
	d.deltap.z = this->deltap.z*num;
	d.deltav.x = this->deltap.x*num;
	d.deltav.y = this->deltap.y*num;
	d.deltav.z = this->deltap.z*num;
	return d;
}

Delta Delta::operator/(double num)
{
	Delta d = Delta();
	d.deltap.x = this->deltap.x/num;
	d.deltap.y = this->deltap.y/num;
	d.deltap.z = this->deltap.z/num;
	d.deltav.x = this->deltap.x/num;
	d.deltav.y = this->deltap.y/num;
	d.deltav.z = this->deltap.z/num;
	return d;
}
