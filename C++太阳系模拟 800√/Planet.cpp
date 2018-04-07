#include"Planet.h"
#include<math.h>
#include<iostream>
#include"constant.h"
#include"Delta.h"
#include"Galaxy.h"

Planet::Planet(std::string name, double mass,double x, double y, double z, double vx, double vy, double vz) {
	this->name = name;
	this->mass = mass;
	this->place.x = x;
	this->place.y = y;
	this->place.z = z;
	this->velocity.x = vx;
	this->velocity.y = vy;
	this->velocity.z = vz;
}

Planet * Planet::update_Euler(Galaxy * galaxy){
	Planet* nextp = new Planet();
	*nextp = *this;
	Delta delta = Delta();
	makedelta(&delta, this, galaxy);
	nextp->adddelta(delta);
	return nextp;
}

Planet * Planet::update_Runge_Kutta(Galaxy * galaxy){
	Planet* nextp =new Planet();
	*nextp = *this;
	Planet tempp1 = Planet();
	Planet tempp2 = Planet();
	Planet tempp3 = Planet();

	Delta delta1 =Delta();
	Delta delta2 =Delta();
	Delta delta3 =Delta();
	Delta delta4 = Delta();
	makedelta(&delta1, this, galaxy);

	tempp1 = *this;
	tempp1.adddelta(delta1*0.5);
	makedelta(&delta2, &tempp1, galaxy);

	tempp2 = *this;
	tempp2.adddelta(delta2*0.5);
	makedelta(&delta3, &tempp2, galaxy);

	tempp3 = *this;
	tempp3.adddelta(delta3*0.5);
	makedelta(&delta4, &tempp3, galaxy);

	nextp->adddelta(delta1 / 6 + delta2 / 3 + delta3 / 3 + delta4 / 6);
	return nextp;
}

void Planet::adddelta(Delta delta){
	this->place = this->place + delta.deltap;
	this->velocity = this->velocity + delta.deltav;
}

double Planet::getdistance(Planet * p2){
	double dx = this->place.x - p2->place.x;
	double dy = this->place.y - p2->place.y;
	double dz = this->place.z - p2->place.z;
	return sqrt(dx*dx + dy * dy + dz * dz);
}

void Planet::makedelta(Delta * delta, Planet * planet,Galaxy* galaxy){
	delta->deltap=(delta->deltav)*DT;
	delta->deltav.init(0.0, 0.0, 0.0);
	for (unsigned int i = 0; i < galaxy->planets.size(); i++) {
		if (galaxy->planets[i]->name != planet->name) {
			delta->deltav = delta->deltav + (galaxy->planets[i]->place - planet->place)*(G * galaxy->planets[i]->mass / getdistance(galaxy->planets[i])*getdistance(galaxy->planets[i])* getdistance(galaxy->planets[i]))*DT;
		}
	}
}

void Planet::show(){
	std::cout << this->name << ":place(" << this->place.x<<","<< this->place.y <<","<< this->place.z <<")";
	std::cout <<":velocity(" << this->velocity.x << "," << this->velocity.y << "," << this->velocity.z << ")" <<std::endl;
}

void Planet::operator=(Planet * p){
	this->name = p->name;
	this->mass = p->mass;
	this->place.x = p->place.x;
	this->place.y = p->place.y;
	this->place.z = p->place.z;
	this->velocity.x = p->velocity.x;
	this->velocity.y = p->velocity.y;
	this->velocity.z = p->velocity.z;
}


Planet::Planet(){
}
