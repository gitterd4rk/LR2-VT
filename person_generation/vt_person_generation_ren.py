import inspect
import renpy
from renpy.exports import write_log
from game.main_character.MainCharacter_ren import mc
from game.major_game_classes.character_related.Person_ren import Person
from game.helper_functions.random_generation_functions_ren import make_person, create_random_person, get_premade_character, create_party_schedule, create_hooker, create_stripper
from game.major_game_classes.character_related._job_definitions_ren import JobDefinition, prostitute_job, stripper_job
from game.major_game_classes.clothing_related.wardrobe_builder_ren import WardrobeBuilder
from typing import Union
day: int

# USE THIS FLAG FOR DEBUG OUTPUTS
VIRGIN_TRACKER_DEBUG = True

"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init 100 python:
"""
import math
import builtins

# helper function; if the person has a sex skill, she must have gotten it with someone
# returns name either random, SO_name, or MC
def _vt_cherry_popper(person) -> str | None:
    if person.relationship != "Single" and person.SO_name is mc.name:
        return mc.name
    elif person.relationship != "Single" and person.SO_name:
        return person.SO_name
    else:
        return Person.get_random_male_name()

def _vt_bounded_gaussian_int(lower=2, upper=8, mean=3.4, stdev=10/3) -> int:
    # NOTE: smaller window between lower and upper
    # (i.e. less area under the curve)
    # means (exponentially) longer while-loop
    value = int(lower) - 1
    while value < lower or value > upper:
        value = int(renpy.random.gauss(mean, stdev))
    return value

def _vt_is_virgin(person: Person, sex_kind: str) -> bool:
    if person.type in ("story", "unique"):
        return person.sex_skills[sex_kind] == 0 or (sex_kind=="Vaginal" and person.sex_skills[sex_kind] == 1)
    elif sex_kind == "Vaginal" and person.kids > 0:
        return False
    else:
        # TODO: make virginity likelihood granular
        # based on sex type (oral/vaginal/anal)?
        VIRGINITY_LIKELIHOOD_BY_AGE: dict[tuple[int | float], dict[str, float]] = {
            # (min age, max age):
            #     {sex kind, virginity probability},
            (-math.inf, Person.get_age_floor() - 1):
                {"Oral": 1.0, "Vaginal": 1.0, "Anal": 1.0},
            (Person.get_age_floor(), 19):
                {"Oral": 0.3, "Vaginal": 0.3, "Anal": 0.3},
            (20, 30):
                {"Oral": 0.3, "Vaginal": 0.3, "Anal": 0.3},
            (31, math.inf):
                {"Oral": 0.1, "Vaginal": 0.1, "Anal": 0.1},
        }
        for (min_age, max_age), virginity_probability in VIRGINITY_LIKELIHOOD_BY_AGE.items():
            if min_age <= person.age <= max_age:
                return renpy.random.random() < virginity_probability[sex_kind]
        # FIXME: should never get this far
        return False

def _vt_virginal_stats(person: Person, sex_kind: str, sex_cap: int) -> dict:
    stats: dict[str, int | str | None] = {}
    # vaginal "just the tip" (skill=1) counts as virgin
    if _vt_is_virgin(person, sex_kind):
        # IN THIS BRANCH: IS A VIRGIN (for that sex kind)
        # set name of first partner in sex kind to None
        stats[sex_kind.lower() + "_first"] = None

        # set sex_skill to 0 (or possibly 1, if sex_kind == "Vaginal")
        if sex_kind == "Vaginal":
            # if vaginal virgin/"just the tip" set hymen to sealed
            stats["hymen"] = 0
            person.sex_skills[sex_kind] = (1 if person.sex_skills["Vaginal"] == 1 else 0)
        else:
            person.sex_skills[sex_kind] = 0

        # set sex_kind virginality to 0
        stats[sex_kind.lower() + "_virgin"] = 0

    else:
        # IN THIS BRANCH: DEFLOWERED (for that sex kind)
        # set name of first partner in sex kind
        stats[sex_kind.lower() + "_first"] = _vt_cherry_popper(person)

        # if vaginal, set hymen to normal
        if sex_kind=="Vaginal":
            stats["hymen"] = 2

        # with this mod, non-virginal means skill >= 2
        if person.sex_skills[sex_kind] <= 2:
            reroll = _vt_bounded_gaussian_int(2, sex_cap)
            #reroll = renpy.random.randint(2, sex_cap)
            person.sex_skills[sex_kind] = reroll
            stats[sex_kind.lower() + "_virgin"] = reroll
        else:
            stats[sex_kind.lower() + "_virgin"] = builtins.min(10, person.sex_skills[sex_kind])
            if sex_kind == "Vaginal" and person.kids != 0 and person.sex_skills[sex_kind] <= 10:
                # FIXME: shouldn't this be setting sex_skills["Vaginal"]
                # instead of "vaginal_virgin"?
                stats[sex_kind.lower() + "_virgin"] = 7 # give mothers an edge

    # always set (oral/vaginal/anal)_cum to 0
    stats[sex_kind.lower() + "_cum"] = 0

    return stats

def _vt_prefix_person_init(wrapped_func):
    def wrapping_func(*args, **kwargs):
        # hack
        # if age (args[3]) <= core game min age (default 18)
        if args[3] <= Person.get_age_floor() and kwargs["type"] not in ("story", "unique"):
            # ensure single with no kids
            kwargs["relationship"] = "Single"
            kwargs["kids"] = 0
        return wrapped_func(*args, **kwargs)
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_postfix_person_run_turn(wrapped_func):
    def wrapping_func(*args, **kwargs):
        # Call core code; has core side effects
        ret_val = wrapped_func(*args, **kwargs)

        self = args[0]
        #VirginTracker cum tracker dealing with cum in orifices
        # NOTE: vaginal_cum has floor 1, other two have floor 0
        if self.oral_cum > 0 and (day -self.sex_record.get("Last Oral Day", -1)) >= 0:
            self.oral_cum -= 1
        if self.anal_cum > 0 and (day -self.sex_record.get("Last Anal Day", -1)) >= 0:
            self.anal_cum -= 1
        if self.vaginal_cum > 1 and (day -self.sex_record.get("Last Vaginal Day", -1)) >= 0:
            self.vaginal_cum -= 1

        return ret_val # probably None, but core could change
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_postfix_person_run_day(wrapped_func):
    def wrapping_func(*args, **kwargs):
        # Call core code; has core side effects
        ret_val = wrapped_func(*args, **kwargs)

        self = args[0]
        # dealing with virgin hymen healing, 0-seal 1-bleeding/torn 2-normalized
        # only heal hymen at day end if haven't had vaginal sex for at least 3 days
        if self.hymen == 1 and (day - self.sex_record.get("Last Vaginal Day", -1)) >= 3:
            self.hymen = 2
        # dealing with muscles relaxing and stretching back to normal levels
        # virgin is None: #0=virgin, 1=just the tip, 2=full penetration, 3-10 is degree of tightness
        # 3 is the normal tightness of the muscles, higher would be from trauma ie, baby -> 5-7
        # will always return to normal after a few days depending on the trauma
        if self.vaginal_virgin > 3 and (day - self.sex_record.get("Last Vaginal Day", -1)) >= 3:
            self.vaginal_virgin -= 1
        if self.oral_virgin > 3 and (day - self.sex_record.get("Last Oral Day", -1)) >= 3:
            self.oral_virgin -= 1
        if self.anal_virgin > 3 and (day - self.sex_record.get("Last Anal Day", -1)) >= 3:
            self.anal_virgin -= 1
        # remove up to one level vaginal cum (only way to remove last level)
        if self.vaginal_cum > 0 and (day - self.sex_record.get("Last Vaginal Day", -1)) >= 4:
            self.vaginal_cum -= 1

        return ret_val # probably None, but core could change
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_postfix_person_cum_in_mouth(wrapped_func):
    def wrapping_func(*args, **kwargs):
        ret_val = wrapped_func(*args, **kwargs)

        self = args[0]
        self.oral_cum += 1

        return ret_val # probably None, but core could change
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_postfix_person_cum_in_vagina(wrapped_func):
    def wrapping_func(*args, **kwargs):
        ret_val = wrapped_func(*args, **kwargs)

        self = args[0]
        self.vaginal_cum += 1

        return ret_val # probably None, but core could change
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_postfix_person_cum_in_ass(wrapped_func):
    def wrapping_func(*args, **kwargs):
        ret_val = wrapped_func(*args, **kwargs)

        self = args[0]
        self.anal_cum += 1

        return ret_val # probably None, but core could change
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_postfix_person_update_sex_record(wrapped_func):
    def wrapping_func(*args, **kwargs):
        ret_val = wrapped_func(*args, **kwargs)

        self, report_log = args
        types_seen = set(position_type.record_class for position_type in report_log.get("positions_used", []))

        # .get(, default=Foreplay) is necessary because standing_grope and drysex_cowgirl do not have record_class
        sex_classes = set(Person._record_skill_map.get(sex_type, "Foreplay") for sex_type in types_seen)
        sex_classes.discard("Foreplay")

        # at this point, sex_classes is guaranteed to be some subset of
        # {"Oral", "Vaginal", "Anal"}
        for sex_class in sex_classes:
            # make the appropriate strings, e.g. "oral_virgin" and "oral_first"
            # using these strings with setattr/getattr allows same code in loop
            _sex_type_first = sex_class.lower() + "_first"
            _sex_type_virgin = sex_class.lower() + "_virgin"

            # set last day had this kind of sex
            self.sex_record["Last " + sex_class + " Day"] = day

            # if _virgin is 0
            if getattr(self, _sex_type_virgin, 3) == 0:
                # set _first name
                setattr(self, _sex_type_first, mc.name)
                # and if vaginal
                if sex_class == "Vaginal":
                    # tear hymen
                    self.hymen = 1

            # if _virgin <= 9 (NOTE: this condition is always evaluated,
            # whether or not the previous `if _virgin == 0`` was True)
            if getattr(self, _sex_type_virgin) <= 9:
                # increase it by one
                setattr(self, _sex_type_virgin, getattr(self, _sex_type_virgin, 3) + 1)

        return ret_val # probably None, but core could change
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

Person.__init__         = _vt_prefix_person_init(Person.__init__)
Person.run_turn         = _vt_postfix_person_run_turn(Person.run_turn)
Person.run_day          = _vt_postfix_person_run_day(Person.run_day)
Person.cum_in_mouth     = _vt_postfix_person_cum_in_mouth(Person.cum_in_mouth)
Person.cum_in_vagina    = _vt_postfix_person_cum_in_vagina(Person.cum_in_vagina)
Person.cum_in_ass       = _vt_postfix_person_cum_in_ass(Person.cum_in_ass)
Person.update_person_sex_record = _vt_postfix_person_update_sex_record(Person.update_person_sex_record)

def _vt_create_random_person_override(wrapped_func):
    def wrapping_func(*args, **kwargs):
        virgin_tracker_args: tuple[str] = (
            "oral_virgin",
            "oral_first",
            #"oral_cum",
            "hymen",
            "vaginal_virgin",
            "vaginal_first",
            #"vaginal_cum",
            "anal_virgin",
            "anal_first",
            #"anal_cum",
        )
        virginity_types = ["Oral", "Vaginal", "Anal"]

        # use this line to keep core game balance
        sex_cap = Person.get_skill_ceiling()

        # else uncomment this line for uniform distribution from 2-8
        #sex_cap = 8

        # override above sex_cap if passed as keyword arg
        if "sex_cap" in kwargs:
            sex_cap = kwargs["sex_cap"]
            kwargs.pop("sex_cap", None)

        # grab any provided VirginTracker keyword args
        # remove them from the kwargs dict
        given_vt_kwargs: dict[str, int | None] = {}
        for arg_name in virgin_tracker_args:
            if arg_name in kwargs:
                given_vt_kwargs[arg_name] = kwargs[arg_name]
                kwargs.pop(arg_name, None)

        # force kids=0 if hymen is sealed or recently torn
        if given_vt_kwargs.get("hymen", None) in (0, 1):
            kwargs["kids"] = 0

        ######################
        #### Call to core code
        ######################
        person = wrapped_func(*args, **kwargs)

        if VIRGIN_TRACKER_DEBUG:
            write_log("Overriding create_random_person; adding attributes")

        # NOTE: this is all-or-nothing; if some but not all of the VT kwargs are provided
        # the provided values will be ignored, and instead all values estimated based on sex skills
        # if create_random_person was called with all the VirginTracker keyword args
        if set(virgin_tracker_args) == set(given_vt_kwargs.keys()):
            for key, value in given_vt_kwargs.items():
                # set the values directly
                setattr(person, key, value)
        else:
            for sex_type in virginity_types:
                # compute the values
                stats = _vt_virginal_stats(person, sex_type, sex_cap)
                # and apply them
                for key, value in stats.items():
                    setattr(person, key, value)

        # set orifice cum to 0
        for sex_type in virginity_types:
            setattr(person, sex_type.lower() + "_cum", 0)

        return person

    # don't override the signature, because modded code might provide VT kwargs
    #wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_make_person_override(wrapped_func):
    def wrapping_func(*args, **kwargs):
        # the below are added to kwargs by this mod:
        # sex_cap=7, hymen = None, vaginal_virgin = 0, anal_virgin = 0, oral_virgin = 0, vaginal_first = None, anal_first = None, oral_first = None

        # ignore wrapped_func because we overwrite it to pass args as desired

        return_character = None
        if type == "random" and kwargs.get("allow_premade") and renpy.random.randint(1, 100) < 20:
            return_character = get_premade_character(kwargs.get("age_range"), kwargs.get("tits_range"), kwargs.get("height_range"), kwargs.get("kids_range"), kwargs.get("relationship_list"))

        if return_character is None: #Either we aren't getting a pre-made, or we are out of them.
            return_character = create_random_person(*args, **kwargs)

        # apply forced opinions after we 'update opinions', so we don't override them there
        if isinstance(kwargs.get("forced_opinions"), list):
            for opinion_name, (opinion_value, opinion_known) in kwargs["forced_opinions"]:
                return_character.opinions[opinion_name] = [opinion_value, opinion_known]

        if isinstance(kwargs.get("forced_sexy_opinions"), list):
            for opinion_name, (opinion_value, opinion_known) in kwargs["forced_sexy_opinions"]:
                return_character.sexy_opinions[opinion_name] = [opinion_value, opinion_known]

        if return_character.base_outfit and len(return_character.base_outfit.accessories) == 0 and return_character.opinion.makeup > 0:
            WardrobeBuilder.add_make_up_to_outfit(return_character, return_character.base_outfit)

        if return_character.type == 'random':
            create_party_schedule(return_character)

        return return_character
    # don't copy signature, because we changed it
    #wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_create_hooker_override(wrapped_func):
    def wrapping_func(*args, **kwargs):
        # change sluttiness range, type="unique", sex_skill_array ranges
        hooker = make_person(sluttiness = renpy.random.randint(30, 55),
            sex_skill_array = [renpy.random.randint(4,8),renpy.random.randint(3,8),renpy.random.randint(2,8),renpy.random.randint(2,8)],
            job = prostitute_job,
            type="unique",
            forced_opinions = [
                ["flirting", 2, True],
                ["high heels", 2, True],
                ["makeup", 1, True],
                ["pants", -2, False],
                ["skirts", 2, True],
            ],
            forced_sexy_opinions = [
                ["bareback sex", -2, True],
                ["being submissive", 1, False],
                ["giving blowjobs", 2, False],
                ["public sex", 2, False],
                ["showing her tits", 1, False],
                ["skimpy outfits", 2, True],
                ["vaginal sex", 2, False],
            ])
        hooker.set_mc_title("Honey")
        if (len(args) > 0 and args[0]) or kwargs.get("add_to_game"):
            hooker.generate_home().add_person(hooker)
        return hooker
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

def _vt_create_stripper_override(wrapped_func):
    def wrapping_func(*args, **kwargs):
        # change sluttiness range, type="unique", sex_skill_array ranges
        stripper = make_person(sluttiness = renpy.random.randint(25, 55),
            sex_skill_array = [renpy.random.randint(4,8),renpy.random.randint(3,8),renpy.random.randint(2,8),renpy.random.randint(2,8)],
            job = stripper_job,
            type="unique",
            forced_opinions = [
                ["small talk", 1, True],
                ["conservative outfits", -2, True],
                ["flirting", 2, True],
                ["high heels", 2, True],
                ["work uniforms", 1, True],
            ], forced_sexy_opinions = [
                ["showing her tits", 2, True],
                ["showing her ass", 2, True],
                ["skimpy outfits", 2, True],
                ["taking control", 2, True],
            ])
        stripper.set_mc_title("Honey")
        stripper.generate_home()
        stripper.home.add_person(stripper)
        return stripper
    wrapping_func.__signature__ = inspect.signature(wrapped_func)
    return wrapping_func

create_random_person = _vt_create_random_person_override(create_random_person)
make_person = _vt_make_person_override(make_person)
create_hooker = _vt_create_hooker_override(create_hooker)
create_stripper = _vt_create_stripper_override(create_stripper)