#include<iostream>
#include<vector>
#include"Galaxy.h"
#include"Planet.h"

Planet Sun=Planet("Sun", 1.989e30,0,0,0,0,0,0);
Planet Earth =Planet("Earth",5.972e24, 1.496e11, 0, 0, 0, 2.978e4, 0);
Planet Venus = Planet("Venus", 4.867e24, -1.082e11, 0, 6.422e9, 0, -3.502e4, 0);
Planet Mars = Planet("Mars", 6.417e23, 0, 2.279e11, 7.359e9, -2.401e4, 0, 0);
Planet Jupiter = Planet("Jupiter", 1.898e27, 0, -7.785e11, -1.77e10, 1.307e4, 0, 0);
Planet Neutronstar = Planet("Neutronstar", 4.0e30, 0, 0, 1.0e15, 1.2e2, 0, -1.0e5);
int main() {
	Galaxy sun_earth_system = Galaxy();
	sun_earth_system.add_planet(&Sun);
	sun_earth_system.add_planet(&Earth);
	Galaxy solarsystem = Galaxy();
	solarsystem.add_planet(&Sun);
	solarsystem.add_planet(&Earth);
	solarsystem.add_planet(&Jupiter);
	solarsystem.add_planet(&Mars);
	solarsystem.add_planet(&Venus);
	Galaxy solarsystem_Neutronstar = Galaxy();
	solarsystem_Neutronstar.add_planet(&Sun);
	solarsystem_Neutronstar.add_planet(&Earth);
	solarsystem_Neutronstar.add_planet(&Jupiter);
	solarsystem_Neutronstar.add_planet(&Mars);
	solarsystem_Neutronstar.add_planet(&Venus);
	solarsystem_Neutronstar.add_planet(&Neutronstar);


	solarsystem_Neutronstar.display_Runge_Kutta(20);
	solarsystem.display_Runge_Kutta(20);
	sun_earth_system.display_Runge_Kutta(20);
	solarsystem_Neutronstar.display_Euler(20);
	solarsystem.display_Euler(20);
	sun_earth_system.display_Euler(20);
	return 0;
}