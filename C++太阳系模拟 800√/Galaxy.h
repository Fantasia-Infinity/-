#pragma once
#ifndef GALAXY
#define GALAXY

#include<iostream>
#include<vector>
#include"Planet.h"

class Galaxy {
public:
	Galaxy();
	~Galaxy();
	std::vector<Planet*> planets;
	void add_planet(Planet* planet);
	void Euler_update();
	void Runge_Kutta_update();
	void show();
	void display_Euler(double time);
	void display_Runge_Kutta(double time);

};


#endif 