#pragma once

#include <string>
#include <vector>

namespace mvg {

	class Station {
	public:
		Station(std::string name) : name_(name) {}
		Station() = default;
		Station(Station const&) = default;
		Station& operator=(Station const&) = default;
		Station(Station&&) = default;
		Station& operator=(Station&&) = default;
	private:	
		std::string name_;
	};

	bool operator<(Station const& l, Station const& r);
	bool operator>(Station const& l, Station const& r);
	bool operator<=(Station const& l, Station const& r);
	bool operator>=(Station const& l, Station const& r);
	bool operator==(Station const& l, Station const& r);
	bool operator!=(Station const& l, Station const& r);

	struct Line {
		std::vector<Station> stations_;
	};

	struct Network {
		std::vector<Station> findRoute(Station const& start, Station const& end);
		std::vector<Line> lines_;
	};

}