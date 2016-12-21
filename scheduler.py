#referenced Wikipedia Ford Fulkerson Algorithm
import argparse
import networkflow 

parser = argparse.ArgumentParser(description='Produces a matching for ANova members.')
parser.add_argument('preferences', help="preferences input")
parser.add_argument('schools', help="schools input")

args = parser.parse_args()

def main():
	people = parse_preferences(args.preferences)
	schools = parse_schools(args.schools)
	school_names = [school[0] for school in schools]
	people_names = [person[0] for person in people]

	g = networkflow.FlowNetwork()
	[g.add_vertex(v) for v in ["s", "t"] + school_names + people_names]
	for person in people:
		name = person[0]
		preferences = person[1:]
		g.add_edge("s", name, 1)
		for preference in preferences:
			g.add_edge(name, preference, 1)

	for school in schools:
		name = school[0]
		flow = school[1]
		g.add_edge(name, "t", flow)

	print(g.max_flow("s", "t", school_names))

def parse_preferences(preferences):
	people = []
	with open (preferences, "r") as file:
		for line in file:
			person = line.strip("\n ").split(",")
			people.append(person)
	return people

def parse_schools(schools):
	values = []
	with open (schools, "r") as file:
		for line in file:
			school = line.strip("\n ").split(",")
			print(school)
			school[1] = int(school[1])
			values.append(school)
	return values

if __name__ == "__main__":
	main()