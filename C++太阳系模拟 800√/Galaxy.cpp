#include"Galaxy.h"
#include"constant.h"
#include<vector>


Galaxy::Galaxy(){
}

Galaxy::~Galaxy(){
	for (unsigned int i = 0; i < this->planets.size(); i++) {
		delete this->planets[i];
	}
}

void Galaxy::add_planet(Planet * planet){
	Planet* p = new Planet();
	*p = planet;
	this->planets.push_back(planet);
}

void Galaxy::Euler_update(){
	std::vector<Planet*> new_planets;
	for (unsigned int i = 0; i < this->planets.size(); i++) {
		Planet* p;
		p = this->planets[i]->update_Euler(this);
		new_planets.push_back(p);
	}
	planets.clear();
	for (unsigned int i = 0; i < new_planets.size(); i++) {
		this->planets.push_back(new_planets[i]);
	}
}

void Galaxy::Runge_Kutta_update(){
	std::vector<Planet*> new_planets;
	for (unsigned int i = 0; i < this->planets.size(); i++) {
		Planet* p;
		p = this->planets[i]->update_Runge_Kutta(this);
		new_planets.push_back(p);
	}

	planets.clear();
	for (unsigned int i = 0; i < new_planets.size(); i++) {
		this->planets.push_back(new_planets[i]);
	}
}

void Galaxy::show(){
	for (unsigned int i = 0; i < this->planets.size(); i++) {
		this->planets[i]->show();
	}
}

void Galaxy::display_Euler(double time){
	int round = (time / (DT));
	for (int i = 0; i < round; i++) {
		this->show();
		this->Euler_update();
		std::cout << std::endl;
	}
}

void Galaxy::display_Runge_Kutta(double time){
	int round = (time / (DT));
	for (int i = 0; i < round; i++) {
		this->show();
		this->Runge_Kutta_update();
		std::cout << std::endl;
	}
}
