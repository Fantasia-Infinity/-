#pragma once
#ifndef PLANET
#define PLANET
#include<vector>
#include<string>
#include"Vector3.h"
#include"Delta.h"


class Galaxy;
class Planet {
public:
	Planet();
	Planet(std::string name,double mass,double x,double y,double z,double vx,double vy,double vz);
	std::string name;
	double mass;
	Vector3 velocity;
	Vector3 place;
	Planet* update_Euler(Galaxy* galaxy);
	Planet* update_Runge_Kutta(Galaxy* galaxy);
	void adddelta(Delta delta);
	double getdistance(Planet* p2);
	void makedelta(Delta* delta, Planet* planet,Galaxy* galaxy);
	void show();
	void operator=(Planet* p);
};
#endif 