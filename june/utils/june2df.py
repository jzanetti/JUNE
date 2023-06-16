from copy import copy as shallow_copy
from copy import deepcopy
from datetime import datetime
from os.path import join

from june.geography.geography import Geography as Geography_class
from june.world import World as World_class
from pandas import DataFrame


SECTOR_CODES = {
    "A": "Agriculture, Forestry and Fishing",
    "B": "Mining",
    "C": "Manufacturing",
    "D": "Electricity, Gas, Water and Waste Services",
    "E": "Construction",
    "F": "Wholesale Trade",
    "G": "Retail Trade",
    "H": "Accommodation and Food Services",
    "I": "Transport, Postal and Warehousing",
    "J": "Information Media and Telecommunications",
    "K": "Financial and Insurance Services",
    "L": "Rental, Hiring and Real Estate Services",
    "M": "Professional, Scientific and Technical Services",
    "N": "Administrative and Support Services",
    "O": "Public Administration and Safety",
    "P": "Education and Training",
    "Q": "Health Care and Social Assistanc",
    "R": "Arts and Recreation Services",
    "S": "Other Services",
}



def get_people_for_groups_df(
    world_input2: World_class,
    time: datetime = None,
    groups: list = [
        "care_homes",
        "cemeteries",
        "cinemas",
        "city_transports",
        "companies",
        "groceries",
        "hospitals",
        "inter_city_transports",
        "households",
        "pubs",
        "schools",
        "universities",
    ],
) -> dict:
    """Get total people for different groups

    Args:
        world_input2 (World_class): World object
        total_people (dict): total people to be exported
        time (Datetime, optional): Time for data. Defaults to None.
        groups (list, optional): Groups to use. Defaults to [
            "care_homes", "cemeteries", "cinemas", "city_transports",
            "companies", "groceries", "hospitals",
            "inter_city_transports", "households",
            "pubs", "schools", "universities" ].

    Returns:
        dict: dict contains people
    """
    world_input = deepcopy(world_input2)

    output = {"area": [], "time": [], "people": [], "group": []}
    for proc_group in groups:
        if proc_group == "cemeteries":
            continue

        proc_data = getattr(world_input, proc_group)

        if proc_data is not None:
            for proc_member in proc_data:
                output["area"].append(proc_member.area.name)
                output["time"].append(time)
                output["people"].append(proc_member.size)
                output["group"].append(proc_group)

    return DataFrame.from_dict(output)


def world_person2df(world_input2, time=None):
    world_input = shallow_copy(world_input2)

    person_info = {
        "time": [],
        "super_area_name": [],
        "area_name": [],
        "id": [],
        "sex": [],
        "age": [],
        "ethnicity": [],
        "comorbidity": [],
        "work_sector": [],
        "sub_sector": [],
        "subgroup_or_activity": [],
        "lockdown_status": [],
        "work_super_area": [],
        "home_super_area": [],
        "work_city": [],
        "home_city": [],
        "transport_method": [],
        "transport_public": [],
        "commute_station_type": [],
        "commute_station_city": [],
        "commute_group_name": [],
        "busy": [],
        "housemates": [],
        "num_housemates": [],
        "residence_group_type": [],
        "residence_subgroup_type": [],
        "residence_external": [],
        "infected": [],
        "infection": [],
        "infection_probability": [],
        "time_of_infection": [],
        "intensive_care": [],
        "symptoms_trajectory": [],
        "symptoms": [],
        "dead": [],
    }

    for proc_person in world_input.people:
        if time is not None:
            person_info["time"].append(time)
        else:
            person_info["time"].append(None)

        person_info["id"].append(proc_person.id)
        person_info["super_area_name"].append(proc_person.super_area.name)

        person_info["area_name"].append(proc_person.area.name)

        try:
            housemates = [person.id for person in proc_person.housemates]
        except AttributeError:
            housemates = None

        person_info["housemates"].append(housemates)
        person_info["sex"].append(proc_person.sex)
        person_info["age"].append(proc_person.age)
        person_info["ethnicity"].append(proc_person.ethnicity)
        if proc_person.sector is not None:
            person_info["work_sector"].append(SECTOR_CODES[proc_person.sector])
        else:
            person_info["work_sector"].append(None)
        person_info["sub_sector"].append(proc_person.sub_sector)
        person_info["lockdown_status"].append(proc_person.lockdown_status)
        person_info["comorbidity"].append(proc_person.comorbidity)
        person_info["busy"].append(proc_person.busy)

        subgroup_name = []
        for subgroup_key in dir(proc_person.subgroups):
            if subgroup_key.startswith("__") or subgroup_key == "iter":
                continue

            if getattr(proc_person.subgroups, subgroup_key) is not None:
                subgroup_name.append(subgroup_key)
        if len(subgroup_name) == 0:
            subgroup_name = []
        person_info["subgroup_or_activity"].append(", ".join(subgroup_name))

        try:
            residence_group_type = proc_person.residence.group.type
        except AttributeError:
            residence_group_type = None

        try:
            residence_subgroup_type = proc_person.residence.group.subgroup_type
        except AttributeError:
            residence_subgroup_type = None

        try:
            residence_external = proc_person.residence.residence
        except AttributeError:
            residence_external = None

        person_info["residence_group_type"].append(residence_group_type)
        person_info["residence_subgroup_type"].append(residence_subgroup_type)
        person_info["residence_external"].append(residence_external)
        person_info["infected"].append(proc_person.infected)

        if proc_person.infection is not None:
            person_info["infection"].append(
                # proc_person.infection
                proc_person.infection.tag.name
            )
            person_info["infection_probability"].append(
                round(proc_person.infection.infection_probability, 5)
            )
            person_info["time_of_infection"].append(
                round(proc_person.infection.time_of_infection, 5)
            )
        else:
            person_info["infection"].append(None)
            person_info["infection_probability"].append(None)
            person_info["time_of_infection"].append(None)

        person_info["intensive_care"].append(proc_person.intensive_care)

        person_info["dead"].append(proc_person.dead)
        if proc_person.symptoms is not None:
            symptoms_trajectory = []
            for proc_traj in proc_person.symptoms.trajectory:
                symptoms_trajectory.append((proc_traj[0], proc_traj[1].name))

            person_info["symptoms_trajectory"].append(str(symptoms_trajectory))
            person_info["symptoms"].append(proc_person.symptoms.tag.name)
        else:
            person_info["symptoms_trajectory"].append(None)
            person_info["symptoms"].append(None)

        if proc_person.work_super_area is not None:
            person_info["work_super_area"].append(proc_person.work_super_area.name)
        else:
            person_info["work_super_area"].append(None)
        person_info["home_super_area"].append(proc_person.super_area.name)

        try:
            num_housemates = len(proc_person.housemates)
        except AttributeError:
            num_housemates = None
        person_info["num_housemates"].append(num_housemates)

        if proc_person.work_city is not None:
            person_info["work_city"].append(proc_person.work_city.name)
        else:
            person_info["work_city"].append(None)

        if proc_person.home_city is not None:
            person_info["home_city"].append(proc_person.home_city.name)
        else:
            person_info["home_city"].append(None)

        if proc_person.mode_of_transport is not None:
            person_info["transport_method"].append(proc_person.mode_of_transport.description)
            person_info["transport_public"].append(proc_person.mode_of_transport.is_public)
        else:
            person_info["transport_method"].append(None)
            person_info["transport_public"].append(None)

        if proc_person.commute is not None:
            person_info["commute_station_type"].append(
                proc_person.commute.group.station.station_type
            )
            person_info["commute_station_city"].append(proc_person.commute.group.station.city)
            person_info["commute_group_name"].append(proc_person.commute.group.name)

            # person_info["commute"].append(proc_person.commute)
        else:
            person_info["commute_station_type"].append(None)
            person_info["commute_station_city"].append(None)
            person_info["commute_group_name"].append(None)

    return DataFrame.from_dict(person_info)


def world2df(
    world_input: World_class,
    time: datetime = None,
    write_csv: bool = False,
    workdir: str = None,
    tag: str = "",
):
    """Convert the world object to a dataframe

    Args:
        world_input (World_class): An world object
        time (datetime, optional): Time to write. Defaults to None.
        write_csv (bool, optional): Read CSV file
        workdir (str, optional): Working directory

    Returns:
        dict: The dict contains the dataframe
    """
    my_world = shallow_copy(world_input)

    all_areas = my_world.areas

    household_info = {
        "super_area_name": [],
        "area_name": [],
        "area_population": [],
        "area_socialeconomic_index": [],
        "composition_type": [],
        "being_visited": [],
        "contains_people": [],
        "coordinates": [],
        "n_residents": [],
        "size": [],
        "type": [],
    }

    person_info = {
        "id": [],
        "time": [],
        "super_area_name": [],
        "area_name": [],
        "household_id": [],
        "sex": [],
        "age": [],
        "ethnicity": [],
        "work_sector": [],
        "sub_sector": [],
        "lockdown_status": [],
        "comorbidity": [],
        "busy": [],
        "work_super_area": [],
        "residence_super_area": [],
        "num_housemates": [],
        "work_city": [],
        "home_city": [],
        "transport_method": [],
        "transport_public": [],
        "commute": [],
        "residence_group_type": [],
        "residence_subgroup_type": [],
        "residence_external": [],
        "infected": [],
        "infection": [],
        "intensive_care": [],
        "symptoms": [],
    }

    cities_info = {
        "work_city_name": [],
        "coordinates": [],
        "num_city_stations": [],
        "num_inter_city_stations": [],
        "travel_within_the_city": [],
        "travel_to_this_city_from_others": [],
    }

    all_citieis = my_world.cities
    if all_citieis is not None:
        for proc_city in all_citieis.members:
            cities_info["work_city_name"].append(proc_city.name)
            cities_info["coordinates"].append(str(proc_city.coordinates))
            if isinstance(proc_city.city_stations, list):
                len_city_stations = 0
            else:
                len_city_stations = len(proc_city.city_stations.members)
            cities_info["num_city_stations"].append(len_city_stations)

            if isinstance(proc_city.city_stations, list):
                len_inter_city_stations = 0
            else:
                len_inter_city_stations = len(proc_city.inter_city_stations.members)

            cities_info["num_inter_city_stations"].append(len_inter_city_stations)
            cities_info["travel_within_the_city"].append(str(proc_city.internal_commuter_ids))
            cities_info["travel_to_this_city_from_others"].append(
                str(
                    proc_city.super_area.closest_inter_city_station_for_city[
                        proc_city.name
                    ].commuter_ids
                )
            )

    for proc_area in all_areas.members:
        super_area_name = proc_area.super_area.name
        area_name = proc_area.name
        area_population = len(proc_area.people)
        area_socialeconomic_index = proc_area.socioeconomic_index

        # Print household
        for proc_household in proc_area.households:
            household_info["super_area_name"].append(super_area_name)
            household_info["area_name"].append(area_name)
            household_info["area_population"].append(area_population)
            household_info["area_socialeconomic_index"].append(area_socialeconomic_index)
            household_info["composition_type"].append(proc_household.composition_type)
            household_info["being_visited"].append(proc_household.being_visited)
            household_info["contains_people"].append(proc_household.contains_people)
            household_info["coordinates"].append(str(proc_household.coordinates))
            household_info["n_residents"].append(proc_household.n_residents)
            household_info["size"].append(proc_household.size)
            household_info["type"].append(proc_household.type)

            for proc_person in proc_household.people:
                if time is not None:
                    person_info["time"].append(time)
                else:
                    person_info["time"].append(None)

                person_info["id"].append(proc_person.id)
                person_info["super_area_name"].append(super_area_name)
                person_info["area_name"].append(area_name)
                person_info["household_id"].append(proc_household.id)
                person_info["sex"].append(proc_person.sex)
                person_info["age"].append(proc_person.age)
                person_info["ethnicity"].append(proc_person.ethnicity)
                person_info["work_sector"].append(proc_person.sector)
                person_info["sub_sector"].append(proc_person.sub_sector)
                person_info["lockdown_status"].append(proc_person.lockdown_status)
                person_info["comorbidity"].append(proc_person.comorbidity)
                person_info["busy"].append(proc_person.busy)
                person_info["residence_group_type"].append(proc_person.residence.group.type)
                person_info["residence_subgroup_type"].append(
                    proc_person.residence.group.subgroup_type
                )
                person_info["residence_external"].append(proc_person.residence.external)
                person_info["infected"].append(proc_person.infected)

                if proc_person.infection is not None:
                    person_info["infection"].append(proc_person.infection)
                else:
                    person_info["infection"].append(None)

                person_info["intensive_care"].append(proc_person.intensive_care)

                if proc_person.symptoms is not None:
                    person_info["symptoms"].append(proc_person.symptoms)
                else:
                    person_info["symptoms"].append(None)

                if proc_person.work_super_area is not None:
                    person_info["work_super_area"].append(proc_person.work_super_area.name)
                else:
                    person_info["work_super_area"].append(None)
                person_info["residence_super_area"].append(proc_person.super_area.name)
                person_info["num_housemates"].append(len(proc_person.housemates))

                if proc_person.work_city is not None:
                    person_info["work_city"].append(proc_person.work_city.name)
                else:
                    person_info["work_city"].append(None)

                if proc_person.home_city is not None:
                    person_info["home_city"].append(proc_person.home_city.name)
                else:
                    person_info["home_city"].append(None)

                if proc_person.mode_of_transport is not None:
                    person_info["transport_method"].append(
                        proc_person.mode_of_transport.description
                    )
                    person_info["transport_public"].append(proc_person.mode_of_transport.is_public)
                else:
                    person_info["transport_method"].append(None)
                    person_info["transport_public"].append(None)

                person_info["commute"].append(proc_person.commute)

    output = {
        "household": DataFrame.from_dict(household_info),
        "person": DataFrame.from_dict(person_info),
        "city": DataFrame.from_dict(cities_info),
    }

    if write_csv:
        for output_key in output:
            output[output_key].to_csv(join(workdir, f"{output_key}_{tag}.csv"))

    return output


def geography2df(geography: Geography_class) -> DataFrame:
    """Convert geography to DataFrame

    Args:
        geography (Geography_class): calculated geography

    Returns:
        DataFrame: geography Dataframe
    """

    all_regions = geography.regions

    geography_info = {
        "region_name": [],
        "super_area_name": [],
        "area_name": [],
        "socialeconomic_index": [],
        "super_area_coords": [],
        "area_coords": [],
    }

    for proc_region in all_regions.members:
        proc_region_name = proc_region.name

        all_super_areas = proc_region.super_areas

        for proc_super_area in all_super_areas:
            proc_super_area_coords = proc_super_area.coordinates

            proc_super_area_name = proc_super_area.name

            all_areas = proc_super_area.areas

            for proc_area in all_areas:
                proc_area_socialeconomic_index = proc_area.socioeconomic_index
                proc_area_coordinates = proc_area.coordinates
                proc_area_name = proc_area.name

                geography_info["region_name"].append(proc_region_name)
                geography_info["super_area_name"].append(proc_super_area_name)
                geography_info["area_name"].append(proc_area_name)
                geography_info["socialeconomic_index"].append(proc_area_socialeconomic_index)
                geography_info["super_area_coords"].append(proc_super_area_coords)
                geography_info["area_coords"].append(proc_area_coordinates)

    return DataFrame.from_dict(geography_info)
