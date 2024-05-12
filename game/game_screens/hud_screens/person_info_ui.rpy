# Override default person_info_ui screen by VREN to show extra information about character
init -2 python:
    @renpy.pure
    def person_info_ui_format_hearts(value):
        heart_value = builtins.abs(value)
        if (heart_value / 4) > 10:
            return get_hearts(heart_value / 4, color = "gold")
        return get_hearts(heart_value)

    def person_info_ui_get_formatted_tooltip(person):
        tooltip = []
        for situation in person.situational_sluttiness:
            ss = person.situational_sluttiness[situation]
            tooltip.append(f"{get_coloured_arrow(ss[0])} {person_info_ui_format_hearts(ss[0])} - {ss[1]}\n")
        return "".join(tooltip)

    def person_info_ui_get_formatted_obedience_tooltip(person):
        tooltip = []
        for situation in person.situational_obedience:
            so = person.situational_obedience[situation]
            tooltip.append(f"{get_coloured_arrow(so[0])} {('+' if so[0] > 0 else '')}{so[0]} Obedience - {so[1]}\n")
        return "".join(tooltip)

    def person_info_ui_get_serum_info_tooltip(person):
        tooltips = []
        for serum in person.serum_effects:
            tooltips.append(f"{serum.name}: {serum.total_duration - serum.duration_counter} Turns Left\n")
        return "\n".join(tooltips)

    def person_info_ui_get_special_role_information(person):
        info_list = []
        fetish_roles = [anal_fetish_role, cum_fetish_role, breeding_fetish_role, exhibition_fetish_role]
        for role in [x for x in person.special_role if not x.hidden and x not in fetish_roles]:
            info_list.append(role.role_name)

        active_fetishes = []
        if anal_fetish_role in person.special_role:
            active_fetishes.append("Anal")
        if cum_fetish_role in person.special_role:
            active_fetishes.append("Cum")
        if breeding_fetish_role in person.special_role:
            active_fetishes.append("Breeding")
        if exhibition_fetish_role in person.special_role:
            active_fetishes.append("Exhibition")

        return (sorted(info_list), active_fetishes)

    def person_info_ui_get_job_title(person):
        title = "Unknown"
        if person.primary_job.job_known:
            title = person.primary_job.job_title
        extra_jobs = []
        if person.side_job and person.side_job.job_known:
            extra_jobs.append(person.side_job.job_title)
        if person.secondary_job and person.secondary_job.job_known:
            extra_jobs.append(person.secondary_job.job_title)
        if extra_jobs:
            return f"{title} {{size=14}}[{', '.join(extra_jobs)}]{{/size}}"
        return title

screen person_info_ui(person): #Used to display stats for a person while you're talking to them.
    tag master_tooltip
    layer "solo" #By making this layer active it is cleared whenever we draw a person or clear them off the screen.
    zorder 200

    default home_hub_name = person.home_hub.formal_name
    default job_title = person_info_ui_get_job_title(person)
    default height_info = height_to_string(person.height)
    default weight_info = get_person_weight_string(person)
    python:
        arousal_info = get_arousal_with_token_string(person.arousal, person.max_arousal)
        energy_info = get_energy_string(person.energy, person.max_energy)
        happiness_info = str(builtins.int(person.happiness))
        love_info = get_love_hearts(person.love, 5)
        sluttiness_info = get_heart_image_list(person.sluttiness, person.effective_sluttiness())
        obedience_info = f"{person.obedience} {{image=triskelion_token_small}} {get_obedience_string(person.obedience)}"
        (role_list, fetish_list) = person_info_ui_get_special_role_information(person)
        fetish_info = ", ".join(fetish_list)

    frame:
        background Transform("gui/topboxVT.png", alpha=persistent.hud_alpha)
        xsize 1100
        ysize 200
        yalign 0.0
        xalign 0.5
        xanchor 0.5
        padding (5, 5)
        hbox:
            xanchor 0.5
            xalign 0.5
            yalign 0.1
            spacing 40
            vbox:
                xmaximum 340
                xminimum 340

                hbox:
                    text format_titles(person) style "menu_text_style" size 30
                    use favourite_toggle_button(person)

                text "Job: [job_title]" style "menu_text_style" xoffset 20

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    xsize 220
                    ysize 100
                    vbox:
                        if len(fetish_list) > 0:
                            text "- Fetishes: [fetish_info]" style "menu_text_style" size 12 xoffset 60

                        for role in role_list:
                            text "- [role]" style "menu_text_style" size 12 xoffset 60

            vbox:
                yoffset 5
                xmaximum 280
                xminimum 280

                textbutton "Arousal: [arousal_info]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip f"When a girl is brought to 100% arousal she will start to climax. Climaxing will make a girl happier and may put them into a Trance if their suggestibility is higher than 0.\nCurrently: {get_arousal_number_string(person.arousal, person.max_arousal)}"
                    action NullAction()
                    sensitive True

                textbutton "Energy: [energy_info]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip f"Energy is spent while having sex, with more energy spent on positions that give the man more pleasure. Some energy comes back each turn, and a lot of energy comes back overnight.\nCurrently {get_energy_number_string(person.energy, person.max_energy)}"
                    action NullAction()
                    sensitive True

                textbutton "Happiness: [happiness_info]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip "The happier a girl the more tolerant she will be of low pay and unpleasant interactions. High or low happiness will return to it's default value over time."
                    action NullAction()
                    sensitive True

                textbutton "Love: [love_info]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip f"Girls who love you will be more willing to have sex when you're in private (as long as they aren't family) and be more devoted to you. Girls who hate you will have a lower effective sluttiness regardless of the situation.\nWhen a girl is not part of your harem, she will slowly loose love until it reaches 80, having sex once every five days will stop the love bleed.\nLove: {get_attention_number_string(person.love, 100)}"
                    action NullAction()
                    sensitive True

                hbox:
                    textbutton "Obedience: [obedience_info]":
                        style "transparent_style"
                        text_style "menu_text_style"
                        tooltip f"Girls with high obedience will listen to commands even when they would prefer not to and are willing to work for less pay. Girls who are told to do things they do not like will lose happiness, low obedience girls are likely to refuse altogether.\nActive modifiers will be shown under {{image=question_mark_small}}.\nDominant girls will bleed 1 obedience a day and any other girl that is not a slave will bleed one obedience per day to 200."
                        action NullAction()
                        sensitive True

                    if bool(person.situational_obedience):
                        textbutton "{image=question_mark_small}":
                            style "transparent_style"
                            tooltip person_info_ui_get_formatted_obedience_tooltip(person)
                            action NullAction()
                            sensitive True

                hbox:
                    textbutton "Sluttiness: [sluttiness_info]":
                        style "transparent_style"
                        text_style "menu_text_style"
                        tooltip f"The higher a girls sluttiness the more slutty actions she will consider acceptable and normal. Temporary sluttiness ({{image=red_heart_token_small}}) is added to her sluttiness based on arousal, active modifiers will be shown under {{image=question_mark_small}}.\nSluttiness: {get_attention_number_string(person.effective_sluttiness(), 100)}"
                        action NullAction()
                        sensitive True

                    if bool(person.situational_sluttiness):
                        textbutton "{image=question_mark_small}":
                            style "transparent_style"
                            tooltip person_info_ui_get_formatted_tooltip(person)
                            action NullAction()
                            sensitive True

            vbox:
                yoffset 5
                xmaximum 200
                xminimum 200

                textbutton "Suggestibility: [person.suggestibility]%":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip "How likely a girl is to slip into a trance when she cums. While in a trance she will be highly suggestible, and you will be able to directly influence her stats, skills, and opinions."
                    action NullAction()
                    sensitive True

                textbutton "Age: [person.age]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip "The age of the girl."
                    action NullAction()
                    sensitive True

                textbutton "Height: [height_info]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    if persistent.use_imperial_system:
                        tooltip "The length of the girl in feet and inches."
                    else:
                        tooltip "The length of the girl in centimetres."
                    action NullAction()
                    sensitive True

                textbutton "Cup size: [person.tits]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    tooltip "The size of the breasts."
                    action NullAction()
                    sensitive True

                textbutton "Weight: [weight_info]":
                    style "transparent_style"
                    text_style "menu_text_style"
                    if persistent.use_imperial_system:
                        tooltip "The weight of the girl in pounds.\nDetermines the body type."
                    else:
                        tooltip "The weight of the girl in kilograms\nDetermines the body type."
                    action NullAction()
                    sensitive True

        imagebutton:
            pos (50, 5)
            idle "gui/extra_images/information.png"
            action Show("person_info_detailed", None, person)
            tooltip f"Detailed Information for {person.fname}"

        if person.has_story:
            imagebutton:
                pos (10, 5)
                idle "gui/extra_images/question.png"
                focus_mask True
                action [
                    Show("story_progress", None, person),
                    Function(draw_mannequin, person, person.outfit)
                ]
                tooltip f"Story Progress for {person.fname}"

        if person.mc_knows_address:
            imagebutton:
                pos (1020, 5)
                idle "home_marker"
                tooltip f"She lives in {home_hub_name}."
                action NullAction()
                sensitive True

        if person.can_clone:
            imagebutton:
                pos (1060, 5)
                idle "dna_sequence"
                tooltip "This person can be cloned."
                action NullAction()
                sensitive True

        if person.is_free_use:
            imagebutton:
                pos (1020, 50)
                idle "stocking_marker"
                tooltip "She is a free-use slut."
                action NullAction()
                sensitive True

        if person.serum_tolerance == 0:
            imagebutton:
                pos (55, 50)
                idle "serum_vial3"
                tooltip "Warning: this person has no tolerance for serums\n" + person_info_ui_get_serum_info_tooltip(person)
                action NullAction()
                sensitive True
        elif person.serum_effects:
            imagebutton:
                pos (55, 50)
                idle ("serum_vial3" if len(person.serum_effects) > person.serum_tolerance
                else "serum_vial2" if len(person.serum_effects) == person.serum_tolerance
                else "serum_vial")
                tooltip person_info_ui_get_serum_info_tooltip(person)
                action NullAction()
                sensitive True

        if person.knows_pregnant:
            imagebutton:
                pos(10, 50)
                idle "feeding_bottle"
                action NullAction()

        if person.bc_status_known and person.is_highly_fertile and perk_system.has_ability_perk("Ovulation Cycle Perception"):
            imagebutton:
                pos(10, 50)
                idle "beezee"
                action NullAction()
                tooltip "She is ovulating and has a higher chance of getting pregnant, based on birth control and desire to get pregnant."
#### Relationship Status
        if person.has_relation_with_mc:
            if person.has_role(harem_role):
                if person.has_role(affair_role):
                    imagebutton:
                        pos(285, 166)
                        idle "parapoly"
                        action NullAction()
                        tooltip "She is part of your polycule, and your paramour."
                else:
                    imagebutton:
                        pos(285, 166)
                        idle "polyamorous"
                        action NullAction()
                        tooltip "She is part of your polycule."
            else:
                if person.has_role(affair_role):
                    imagebutton:
                        pos(285, 166)
                        idle "paramour"
                        action NullAction()
                        tooltip "She is your paramour."
                else:
                    imagebutton:
                        pos(285, 166)
                        idle "girlfriend"
                        action NullAction()
                        tooltip "She is your girlfriend."              
        else:
            imagebutton:
                pos(285, 166)
                idle "norelations"
                action NullAction()
                tooltip "No romantic relations with this person?"
### Teen Flag
        if person.age<19:
            imagebutton:
                pos(322, 166)
                idle "matureteen"
                action NullAction()
                tooltip "She looks so innocent and inexperienced."
###### Birth Control Status
        if person.bc_status_known:
            if person.on_birth_control:
                imagebutton:
                    pos(359, 166)
                    idle "birthcontrol"
                    action NullAction()
                    tooltip "She is on birth control."
            else:
                imagebutton:
                    pos(359, 166)
                    idle "nobirthcontrol"
                    action NullAction()
                    tooltip "She is not on birth control."
                if person.is_highly_fertile:
                    imagebutton:
                        pos(359, 166)
                        idle "beezee"
                        action NullAction()
                        tooltip "She is not on birth control and highly fertile."
        else:
            imagebutton:
                pos(359, 166)
                idle "knowbirthcontrol"
                action NullAction()
                tooltip "Don't know if she is on birth control... maybe ask?"
####### Wants Condom
        $ NeedsCondoms = ""
        if person.sexy_opinions.get("bareback sex")==None:
            imagebutton:
                pos(396, 166)
                idle "knowcondom"
                action NullAction()
                tooltip "Does she like bareback sex?"
        else:
            if person.sexy_opinions.get("bareback sex")[1]==True:
                if person.opinion.bareback_sex >= 2 and person.wants_creampie and person.has_cum_fetish and person.has_anal_fetish and person.has_breeding_fetish and person.wants_condom()==False:
                    imagebutton:
                        pos(396, 166)
                        idle "ahegaocondom"
                        action NullAction()
                        tooltip "She loves it raw!"
                else:
                    if person.opinion.bareback_sex >= 2 and person.wants_condom()==False:
                        if person.has_anal_fetish==False:
                            $ NeedsCondoms += f"\n{{image=ahegaoanal_small}} Needs the Anal Fetish Unlocked." 
                        if person.has_breeding_fetish==False:
                            $ NeedsCondoms += f"\n{{image=ahegaovag_small}} Needs the Breeding Fetish Unlocked."
                        if person.has_cum_fetish==False:
                            $ NeedsCondoms += f"\n{{image=ahegaomouth_small}} Needs the Cum Fetish Unlocked."
                        imagebutton:
                            pos(396, 166)
                            idle "nocondom"
                            action NullAction()
                            tooltip "She seems to love raw sex! "+NeedsCondoms
                    else:
                        if person.opinion.bareback_sex >0:
                            $ NeedsCondoms += f"\n{{image=question_mark_small}} Make her love raw sex more!"
                            imagebutton:
                                pos(396, 166)
                                idle "wearcondom"
                                action NullAction()
                                tooltip "Open her mind up to the possibility of more!"+NeedsCondoms
                        else:
                            if person.opinion.bareback_sex == 0:
                                imagebutton:
                                    pos(396, 166)
                                    idle "wearcondom"
                                    action NullAction()
                                    tooltip "She's indifferent to raw sex, so make her like it..."
                            else:
                                if person.opinion.bareback_sex == -2:
                                    $ NeedsCondoms += f"hates"
                                if person.opinion.bareback_sex == -1:
                                    $ NeedsCondoms += f"dislikes"
                                imagebutton:
                                    pos(396, 166)
                                    idle "nocondom"
                                    action NullAction()
                                imagebutton:
                                    pos(396, 166)
                                    idle "dislike"
                                    action NullAction()
                                    tooltip "She "+NeedsCondoms+" raw sex!"
            else:
                imagebutton:
                    pos(396, 166)
                    idle "knowcondom"
                    action NullAction()
                    tooltip "Does she like bareback sex?"
###### Threesome Flag - being fingered - getting head - giving handjobs - vaginal sex - anal sex - being covered in cum
        $ NeedsPolyFetish = ""
        if person.sexy_opinions.get("threesomes")==None:
            imagebutton:
                pos(433, 166)
                idle "knowthreesome"
                action NullAction()
                tooltip "Does she like threesomes?"
        else:
            if person.sexy_opinions.get("threesomes")[1]==True:
                if person.opinion.threesomes >=2 and person.has_cum_fetish and person.has_anal_fetish:
                    imagebutton:
                        pos(433, 166)
                        idle "ahegaothreesomes"
                        action NullAction()
                        tooltip "More the merrier! The mess we will make!"
                else:
                    if person.opinion.threesomes >=2:
                        if person.has_role(harem_role)==False:
                            if person.love <80:
                                $ NeedsPolyFetish += "\nNeeds more loving to be added to your polycule!"
                            else:
                                $ NeedsPolyFetish += "\nShe is ready to be part of your polycule!"
                        if person.has_anal_fetish==False:
                            $ NeedsPolyFetish += f"\n{{image=ahegaoanal_small}} Needs the Anal Fetish Unlocked." 
                        if person.has_cum_fetish==False:
                            $ NeedsPolyFetish += f"\n{{image=ahegaomouth_small}} Needs the Cum Fetish Unlocked."
                        imagebutton:
                            pos(433, 166)
                            idle "threesometriad"
                            action NullAction()
                            tooltip "Open her mind up to more!"+NeedsPolyFetish
                    else:
                        if person.opinion.threesomes >0:
                            $ NeedsPolyFetish += f"\n{{image=question_mark_small}} Make her love threesomes!"
                            imagebutton:
                                pos(433, 166)
                                idle "opentriad"
                                action NullAction()
                                tooltip "Open her mind up to the possibility of more!"+NeedsPolyFetish
                        else:
                            if person.opinion.threesomes == 0:
                                imagebutton:
                                    pos(433, 166)
                                    idle "opentriad"
                                    action NullAction()
                                    tooltip "She's indifferent to threesomes, so make her like it..."
                            else:
                                if person.opinion.threesomes == -2:
                                    $ NeedsPolyFetish += f"hates"
                                if person.opinion.threesomes == -1:
                                    $ NeedsPolyFetish += f"dislikes"
                                imagebutton:
                                    pos(433, 166)
                                    idle "opentriad"
                                    action NullAction()
                                imagebutton:
                                    pos(433, 166)
                                    idle "dislike"
                                    action NullAction()
                                    tooltip "She "+NeedsPolyFetish+" threesomes!"
            else:
                imagebutton:
                    pos(433, 166)
                    idle "knowthreesome"
                    action NullAction()
                    tooltip "Does she like threesomes?"
##### Wants Creampies
        $ NeedsCreampies = ""
        if person.wants_creampie and person.known_opinion("creampies") and person.known_opinion("anal_creampies") and (person.has_anal_fetish and person.has_breeding_fetish) and (person.opinion.anal_creampies >= 2 and person.known_opinion("anal creampies")) and (person.opinion.creampies >= 2 and person.known_opinion("creampies")):
            imagebutton:
                pos(470, 166)
                idle "ahegaopeach"
                action NullAction()
                tooltip "She wants to be filled!"
        else:
            if (person.opinion.anal_creampies >= 1 and person.known_opinion("anal creampies")) or (person.opinion.creampies >= 1 and person.known_opinion("creampies")):
                if person.known_opinion("anal creampies")==False or person.opinion.anal_creampies < 2:
                    $ NeedsCreampies += f"\n{{image=question_mark_small}} Make her love anal creampies!"
                if person.known_opinion("creampies")==False or person.opinion.creampies < 2:
                    $ NeedsCreampies += f"\n{{image=question_mark_small}} Make her love vaginal creampies!"
                if person.has_anal_fetish==False:
                    $ NeedsCreampies += f"\n{{image=ahegaoanal_small}} Needs the Anal Fetish Unlocked." 
                if person.has_breeding_fetish==False:
                    $ NeedsCreampies += f"\n{{image=ahegaovag_small}} Needs the Breeding Fetish Unlocked."
                imagebutton:
                    pos(470, 166)
                    idle "openpeach"
                    action NullAction()
                    tooltip "Keep giving her the cream fillings!"+NeedsCreampies
            else:
                if person.known_opinion("anal creampies") or person.known_opinion("creampies"):
                    if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 1) or (person.known_opinion("creampies") and person.opinion.creampies <1):
                        if person.known_opinion("anal creampies")==False or person.opinion.anal_creampies < 2:
                            $ NeedsCreampies += f"\n{{image=question_mark_small}} Make her like anal creampies!"
                        if person.known_opinion("creampies")==False or person.opinion.creampies < 2:
                            $ NeedsCreampies += f"\n{{image=question_mark_small}} Make her like vaginal creampies!"
                        imagebutton:
                            pos(470, 166)
                            idle "yespeach"
                            action NullAction()
                            tooltip "Doesn't seem to like creampies?"+NeedsCreampies
                    if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 0) or (person.known_opinion("creampies") and person.opinion.creampies <0):
                        if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 1):
                            $ NeedsCreampies = f"anal creampies!"
                        if (person.known_opinion("creampies") and person.opinion.creampies <1):
                            $ NeedsCreampies = f"vaginal creampies!"
                        if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 1) and (person.known_opinion("creampies") and person.opinion.creampies <1):
                            $ NeedsCreampies = f"creampies!"
                        imagebutton:
                            pos(470, 166)
                            idle "dislike"
                            action NullAction()
                            tooltip "She hates "+NeedsCreampies
                else:
                    imagebutton:
                        pos(470, 166)
                        idle "knowpeach"
                        action NullAction()
                        tooltip "Don't know if she likes creampies, ask her?"
###### Cum Fetish
        $ NeedsCumFetish = ""
        if person.sexy_opinions.get("giving blowjobs")==None:
            imagebutton:
                pos(507, 166)
                idle "knowlips"
                action NullAction()
                tooltip "Does she like giving blow jobs?"
        else:
            if person.sexy_opinions.get("giving blowjobs")[1]==True:
                if person.has_cum_fetish:
                    imagebutton:
                        pos(507, 166)
                        idle "ahegaomouth"
                        action NullAction()
                        tooltip "Paint me! Fill me! Feed me! More cummies!"     
                else:
                    if person.oral_sex_skill >= 5 and person.opinion.giving_blowjobs >= 2 and (person.opinion.drinking_cum >= 2 or person.opinion.cum_facials >= 2):
                        if person.cum_exposure_count<19:
                            $ NeedsCumFetish += f"\n{{image=question_mark_small}} Feed her, spray her, or fill her with your cum \n"+ str(19 - person.cum_exposure_count)+" more times!" 
                        else:
                            $ NeedsCumFetish += "\nWait for the event to trigger!"
                        imagebutton:
                            pos(507, 166)
                            idle "openmouth"
                            action NullAction()
                            tooltip "Loves your cum!"+NeedsCumFetish
                    else:
                        if person.opinion.giving_blowjobs >= 2 and ((person.opinion.drinking_cum >= 2 and person.known_opinion("drinking cum")) or (person.opinion.cum_facials >= 2 and person.known_opinion("cum facials"))):
                            if person.oral_sex_skill<5:
                                $ NeedsCumFetish += f"\n{{image=question_mark_small}} Train her oral skills "+ str(5 - person.oral_sex_skill)+" more times!\nIncrease her Hoover Power!"
                            imagebutton:
                                pos(507, 166)
                                idle "bitelip"
                                action NullAction()
                                tooltip "Train her oral skills to vacuum and polish you like a pro!"+NeedsCumFetish
                        else:
                            if person.opinion.giving_blowjobs >= 1:
                                if person.known_opinion("drinking cum")==False:
                                    $ NeedsCumFetish += f"\n{{image=question_mark_small}} Needs her opinion on drinking cum."
                                if person.known_opinion("cum facials")==False:
                                    $ NeedsCumFetish += f"\n{{image=question_mark_small}} Needs her opinion on cum facials."
                                if person.opinion.giving_blowjobs < 2:
                                    $ NeedsCumFetish += f"\n{{image=question_mark_small}} Need her to love giving blowjobs."
                                if person.opinion.drinking_cum < 2:
                                    $ NeedsCumFetish += f"\n{{image=question_mark_small}} Need her to love drinking cum."
                                if person.opinion.cum_facials < 2:
                                    $ NeedsCumFetish += f"\n{{image=question_mark_small}} Need her to love cum facials."
                                imagebutton:
                                    pos(507, 166)
                                    idle "pinklips"
                                    action NullAction()
                                    tooltip "Make her become your cum Queen!"+NeedsCumFetish
                            else:
                                if person.opinion.giving_blowjobs == 0:
                                    imagebutton:
                                        pos(507, 166)
                                        idle "pinklips"
                                        action NullAction()
                                        tooltip "She's indifferent to oral, so make her like it..."
                                else:
                                    if person.opinion.giving_blowjobs == -2:
                                        $ NeedsCumFetish += f"hates"
                                    if person.opinion.giving_blowjobs == -1:
                                        $ NeedsCumFetish += f"dislikes"
                                    imagebutton:
                                        pos(507, 166)
                                        idle "openmouth"
                                        action NullAction()
                                    imagebutton:
                                        pos(507, 166)
                                        idle "dislike"
                                        action NullAction()
                                        tooltip "She "+NeedsCumFetish+" oral!"
            else:
                imagebutton:
                    pos(507, 166)
                    idle "knowlips"
                    action NullAction()
                    tooltip "Does she like giving blow jobs?"
###### Anal Fetish anal_sex_skill >= 5 .anal_sex_count > 19 or self.anal_creampie_count > 19
        $ NeedsAnalFetish = ""
        if person.sexy_opinions.get("anal sex")==None:
            imagebutton:
                pos(544, 166)
                idle "knowpeach"
                action NullAction()
                tooltip "What is her thoughts on anal sex?"
        else:
            if person.sexy_opinions.get("anal sex")[1]==True:
                if person.has_anal_fetish:
                    imagebutton:
                        pos(544, 166)
                        idle "ahegaopeach"
                        action NullAction()
                        tooltip "mmmm Fill my bowels full of your cum!"     
                else:
                    if person.anal_sex_skill >= 5 and (person.opinion.anal_sex >= 2  or person.opinion.anal_creampies >= 2):
                        if (person.anal_sex_count<20 or person.anal_creampie_count<20):
                            $ NeedsAnalFetish = "\nFill her bowels full of cum "+str(19 - person.anal_creampie_count)+" more times!\nHave anal sex with her "+str(19 - person.anal_sex_count)+" more times!"
                        if (person.anal_sex_count==20 or person.anal_creampie_count==20):
                            $ NeedsAnalFetish = "\nWait for the event to trigger!"
                        imagebutton:
                            pos(544, 166)
                            idle "handass"
                            action NullAction()
                            tooltip "Sodomize your Anal Queen!"+NeedsAnalFetish
                    else:
                        if (person.opinion.anal_creampies >= 1 and person.known_opinion("anal creampies")) or person.opinion.anal_sex >= 1:
                            if person.anal_sex_skill <5:
                                $ NeedsAnalFetish += f"\n{{image=question_mark_small}} Train her anal sex skill "+ str(5 - person.anal_sex_skill)+" more times!"
                            if person.known_opinion("anal creampies")==False:
                                $ NeedsAnalFetish += f"\n{{image=question_mark_small}} Need her opinion on anal creampies."
                            if person.opinion.anal_creampies <2:
                                $ NeedsAnalFetish += f"\n{{image=question_mark_small}} Need her to love anal creampies."
                            if person.opinion.anal_sex <2:
                                $ NeedsAnalFetish += f"\n{{image=question_mark_small}} Need her to love anal sex."
                            imagebutton:
                                pos(544, 166)
                                idle "yesanal"
                                action NullAction()
                                tooltip "Train her into your Anal Queen!"+NeedsAnalFetish 
                        else:
                            if person.opinion.anal_sex == 0:
                                imagebutton:
                                    pos(544, 166)
                                    idle "bodyconcealed"
                                    action NullAction()
                                    tooltip "She's indifferent to public sex, so make her like it..."
                            else:
                                if person.opinion.anal_sex == -2:
                                    $ NeedsAnalFetish += f"hates"
                                if person.opinion.anal_sex == -1:
                                    $ NeedsAnalFetish += f"dislikes"
                                imagebutton:
                                    pos(544, 166)
                                    idle "yespeach"
                                    action NullAction()
                                imagebutton:
                                    pos(544, 166)
                                    idle "dislike"
                                    action NullAction()
                                    tooltip "She "+NeedsAnalFetish+" anal!"
            else:
                imagebutton:
                    pos(544, 166)
                    idle "knowpeach"
                    action NullAction()
                    tooltip "What is her thoughts on anal sex?"
###### Breeding Fetish
        $ NeedsBreeding = ""
        if person.sexy_opinions.get("vaginal sex")==None:
            imagebutton:
                pos(581, 166)
                idle "knowpeach"
                action NullAction()
                tooltip "Does she like vaginal sex?"
        else:
            if person.sexy_opinions.get("vaginal sex")[1]==True:
                if person.has_breeding_fetish:
                    imagebutton:
                        pos(581, 166)
                        idle "ahegaovag"
                        action NullAction()
                        tooltip "Breed me! I need your cum!"     
                else:
                    if person.vaginal_sex_skill >= 5 and person.opinion.vaginal_sex >= 2  and person.opinion.creampies >= 2 and person.known_opinion("creampies"):
                        if person.vaginal_creampie_count<20:
                            $ NeedsBreeding += f"\n{{image=question_mark_small}} Fill her full of cum "+ str(20 - person.vaginal_creampie_count)+" more times!"
                        else:
                            $ NeedsBreeding += "\nWait for the event to trigger!"
                        imagebutton:
                            pos(581, 166)
                            idle "openvag"
                            action NullAction()
                            tooltip "She loves your cum! "+NeedsBreeding
                    else:
                        if person.opinion.vaginal_sex >= 2  and (person.opinion.creampies >= 2 and person.known_opinion("creampies")):
                            if person.vaginal_sex_skill <5:
                                $ NeedsBreeding += f"\n{{image=question_mark_small}} Needs her vaginal sex skill raised to 5."
                            if person.opinion.creampies <2:
                                $ NeedsBreeding += f"\n{{image=question_mark_small}} Need her to love vaginal creampies."
                            imagebutton:
                                pos(581, 166)
                                idle "spreadvag"
                                action NullAction()
                                tooltip "Train her vaginal sex skills!" + NeedsBreeding
                        else:            
                            if (person.opinion.creampies >= 1 and person.known_opinion("creampies")) or person.opinion.vaginal_sex >= 1:
                                if person.known_opinion("creampies")==False:
                                    $ NeedsBreeding += f"\n{{image=question_mark_small}} Need her opinion on vaginal creampies."
                                if person.known_opinion("vaginal sex")==False:
                                    $ NeedsBreeding += f"\n{{image=question_mark_small}} Need her opinion on vaginal sex."
                                if person.vaginal_sex_skill <2:
                                    $ NeedsBreeding += f"\n{{image=question_mark_small}} Needs her vaginal sex skill raised to 2."
                                if person.opinion.vaginal_sex < 2:
                                    $ NeedsBreeding += f"\n{{image=question_mark_small}} Need her opinion on vaginal sex to be positive."
                                if person.opinion.creampies < 2:
                                    $ NeedsBreeding += f"\n{{image=question_mark_small}} Need her opinion on vaginal creampies to be positive."
                                imagebutton:
                                    pos(581, 166)
                                    idle "vagclosed"
                                    action NullAction()
                                    tooltip "Train her into your Breeding Stock!"+NeedsBreeding
                            else:
                                if person.opinion.vaginal_sex == 0:
                                    imagebutton:
                                        pos(581, 166)
                                        idle "vagclosed"
                                        action NullAction()
                                        tooltip "She's indifferent to vaginal sex, so make her like it..."
                                else:
                                    if person.opinion.vaginal_sex == -2:
                                        $ NeedsBreeding += f"hates"
                                    if person.opinion.vaginal_sex == -1:
                                        $ NeedsBreeding += f"dislikes"
                                    imagebutton:
                                        pos(581, 166)
                                        idle "vagclosed"
                                        action NullAction()
                                    imagebutton:
                                        pos(581, 166)
                                        idle "dislike"
                                        action NullAction()
                                        tooltip "She "+NeedsBreeding+" vaginal sex!"
            else:
                imagebutton:
                    pos(581, 166)
                    idle "knowpeach"
                    action NullAction()
                    tooltip "Does she like vaginal sex?"
######## Exhibitionist Fetish
        $ NeedsMoreExhibitionist = ""
        if person.sexy_opinions.get("public sex")==None:
            imagebutton:
                pos(618, 166)
                idle "knowbody"
                action NullAction()
                tooltip "Does she like public sex?"
        else:
            if person.sexy_opinions.get("public sex")[1]==True:
                if person.opinion.public_sex >=2 and person.opinion.not_wearing_underwear >= 2 and person.opinion.not_wearing_anything >= 2  and person.known_opinion("not wearing underwear") and person.known_opinion("not wearing anything") and person.opinion.showing_her_ass >= 2 and person.opinion.showing_her_tits >= 2  and person.known_opinion("showing her ass") and person.known_opinion("showing her tits") and person.opinion.skimpy_outfits >= 2 and person.opinion.skimpy_uniforms >= 2 and person.known_opinion("skimpy outfits") and person.known_opinion("skimpy uniforms"):
                    imagebutton:
                        pos(618, 166)
                        idle "ahegaoex"
                        action NullAction()
                        tooltip "My skin needs to breathe and be free!"     
                else:
                    if person.opinion.not_wearing_underwear >= 2 and person.opinion.not_wearing_anything >= 2  and person.known_opinion("not wearing underwear") and person.known_opinion("not wearing anything") and person.opinion.skimpy_outfits >= 2 and person.opinion.skimpy_uniforms >= 2 and person.known_opinion("skimpy outfits") and person.known_opinion("skimpy uniforms"):
                        if person.opinion.public_sex <2:
                            $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Needs to be more comfortable having public sex."
                        if person.known_opinion("showing her ass")==False:
                            $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know her opinion on showing her ass."
                        if person.known_opinion("showing her tits")==False:
                            $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know her opinion on showing her tits."
                        if person.opinion.showing_her_ass <2:
                            $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Needs to be more comfortable showing her ass." 
                        if person.opinion.showing_her_tits <2:
                            $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Needs to be more comfortable showing her tits."
                        imagebutton:
                            pos(618, 166)
                            idle "nudebody"
                            action NullAction()
                            tooltip "Needs to be comfortable having sex in public!"+NeedsMoreExhibitionist
                    else:
                        if person.opinion.skimpy_outfits >= 2 and person.opinion.skimpy_uniforms >= 2 and person.known_opinion("skimpy outfits") and person.known_opinion("skimpy uniforms"):
                            if person.known_opinion("not wearing underwear")==False:
                                $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know her opinion on not wearing underwear."
                            if person.known_opinion("not wearing anything")==False:
                                $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know her opinion on not wearing anything."
                            if person.opinion.not_wearing_underwear <2:
                                $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Needs to be more comfortable wearing no underwear." 
                            if person.opinion.not_wearing_anything <2:
                                $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Needs to be more comfortable not wearing anything."
                            imagebutton:
                                pos(618, 166)
                                idle "underwear"
                                action NullAction()
                                tooltip "Train her to be more comfortable not wearing underwear.. How about nothing at all?!" + NeedsMoreExhibitionist
                        else:
                            if person.opinion.public_sex >0:
                                if person.known_opinion("skimpy outfits")==False:
                                    $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know her opinion on skimpy outfits."
                                if person.known_opinion("skimpy uniforms")==False:
                                    $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know her opinion on skimpy uniforms."
                                if person.known_opinion("public sex")==False:
                                    $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Need to know if she likes public sex."
                                 
                                if person.opinion.skimpy_uniforms <2:
                                    $ NeedsMoreExhibitionist += f"\n{{image=question_mark_small}} Needs to be more comfortable in skimpy uniforms."
                                imagebutton:
                                    pos(618, 166)
                                    idle "bodyconcealed"
                                    action NullAction()
                                    tooltip "She is so shy! Train her into a beautiful Exhibitionist!"+NeedsMoreExhibitionist 
                            else:
                                if person.opinion.public_sex == 0:
                                    imagebutton:
                                        pos(618, 166)
                                        idle "bodyconcealed"
                                        action NullAction()
                                        tooltip "She's indifferent to public sex, so make her like it..."
                                else:
                                    if person.opinion.public_sex == -2:
                                        $ NeedsMoreExhibitionist += f"hates"
                                    if person.opinion.public_sex == -1:
                                        $ NeedsMoreExhibitionist += f"dislikes"
                                    imagebutton:
                                        pos(618, 166)
                                        idle "bodyconcealed"
                                        action NullAction()
                                    imagebutton:
                                        pos(618, 166)
                                        idle "dislike"
                                        action NullAction()
                                        tooltip "She "+NeedsMoreExhibitionist+" public sex!"
            else:
                imagebutton:
                    pos(618, 166)
                    idle "knowbody"
                    action NullAction()
                    tooltip "Does she like public sex?"
        #hymen is 0 = sealed, 1=recently torn bleeding, 2=normal - serum to regenerate vaginal and hymen
        #0=virgin, 1=just the tip, 2=full penetration, 3-10 is degree of tightness
### Oral Virgin Flag
        $ OralArousal = ""            
        if person.oral_virgin == 0:
            $ OralArousal = "looks at you with lust \n in her innocent hungry eyes"
            imagebutton:
                pos(678, 166)
                idle "truevirgin"
                action NullAction()
                tooltip "Her lips seem to beckon you..."
        else:
            if person.oral_first == mc.name:
                $ OralArousal = "starts to drool \n and undress you with her eyes"
            else:
                $ OralArousal = "looks at you with savage lust in her eyes"
        #the interactive icons during sex stuff
        if 'position_choice' in globals():
            if hasattr(position_choice, 'skill_tag'):
                if position_choice.skill_tag == 'Oral':
                    if mc.recently_orgasmed == True and person.oral_cum >=1:
                        imagebutton:
                            pos(678, 166)
                            idle "ahegaomouth"
                            action NullAction()
                            tooltip "You flood her belly with your cum."
                    else:
                        imagebutton:
                            pos(678, 166)
                            idle "openmouth"
                            action NullAction()
                            tooltip "You fuck her mouth with your cock."
                else:
                    if hasattr(position_choice, 'name'):
                        if position_choice.name == 'Kissing':
                            imagebutton:
                                pos(678, 166)
                                idle "pinklips"
                                action NullAction()
                                tooltip "In the throes of kissing you."
                        else:
                            if person.arousal_perc >= 59 and person.oral_cum<=0:
                                imagebutton:
                                    pos(678, 166)
                                    idle "ahegaoface"
                                    action NullAction()
                                    tooltip "She "+OralArousal+"."
                            else:
                                if person.oral_cum >0:
                                    if person.oral_cum == 1:
                                        imagebutton:
                                            pos(678, 166)
                                            idle "ahegaomouth"
                                            action NullAction()
                                            tooltip "She has a dose of your protein in her belly."
                                    else:
                                        imagebutton:
                                            pos(678, 166)
                                            idle "ahegaoface"
                                            action NullAction()
                                            tooltip "Has "+ str(person.oral_cum) +" doses of your cum\n swimming in her belly."
                                else:
                                    if person.oral_first == mc.name:
                                        imagebutton:
                                            pos(678, 166)
                                            idle "claimedmouth"
                                            action NullAction()
                                            tooltip "You Claimed this Pie Hole!"
                                    else:
                                        if person.oral_first !=None:
                                            imagebutton:
                                                pos(678, 166)
                                                idle "knowlips"
                                                action NullAction()
                                                tooltip "Someone else had her lips before you... CLAIM IT!"
            else:
                if person.arousal_perc >= 59 and person.oral_cum<=0:
                    imagebutton:
                        pos(678, 166)
                        idle "ahegaoface"
                        action NullAction()
                        tooltip "She "+OralArousal+"."
                else:
                    if person.oral_cum >0:
                        if person.oral_cum == 1:
                                imagebutton:
                                    pos(678, 166)
                                    idle "ahegaomouth"
                                    action NullAction()
                                    tooltip "She has a dose of your protein in her belly."
                        else:
                            imagebutton:
                                pos(678, 166)
                                idle "ahegaoface"
                                action NullAction()
                                tooltip "Has "+ str(person.oral_cum) +" doses of your cum\n swimming in her belly."
                    else:
                        if person.oral_first == mc.name:
                            imagebutton:
                                pos(678, 166)
                                idle "claimedmouth"
                                action NullAction()
                                tooltip "You Claimed this Pie Hole!"
                        else:
                            if person.oral_first !=None:
                                imagebutton:
                                    pos(678, 166)
                                    idle "knowlips"
                                    action NullAction()
                                    tooltip "Someone else had her lips before you... CLAIM IT!"
        else:
            if person.arousal_perc >= 59 and person.oral_cum<=0:
                imagebutton:
                    pos(678, 166)
                    idle "ahegaoface"
                    action NullAction()
                    tooltip "She "+OralArousal+"."
            else:
                if person.oral_cum >0:
                    if person.oral_cum == 1:
                            imagebutton:
                                pos(678, 166)
                                idle "ahegaomouth"
                                action NullAction()
                                tooltip "She has a dose of your protein in her belly."
                    else:
                        imagebutton:
                            pos(678, 166)
                            idle "ahegaoface"
                            action NullAction()
                            tooltip "Has "+ str(person.oral_cum) +" doses of your cum \n swimming in her belly."
                else:
                    if person.oral_first == mc.name:
                        imagebutton:
                            pos(678, 166)
                            idle "claimedmouth"
                            action NullAction()
                            tooltip "You Claimed this Pie Hole!"
                    else:
                        if person.oral_first !=None:
                            imagebutton:
                                pos(678, 166)
                                idle "knowlips"
                                action NullAction()
                                tooltip "Someone else had her lips before you... CLAIM IT!"
### Anal Virgin Flag
        $ AnalArousal = ""            
        if person.anal_virgin == 0:
            $ AnalArousal = "Her ass sways so ripely, ready for the taking"
            imagebutton:
                pos(715, 166)
                idle "truevirgin"
                action NullAction()
                tooltip "Her ass looks so ripe for the taking."
        else:
            if person.anal_first == mc.name:
                $ AnalArousal = "ass sways, hypnotizing you while \nshe rubs it!"
            else:
                $ AnalArousal = "ass sways and she spreads her ass for you.\nCome take me!"
            if person.anal_virgin >=4:
                $ AnalArousal = "ass sways and she spreads her gaping asshole for you.\nCome take me!"
        #the interactive icons during sex stuff
        if 'position_choice' in globals():
            if hasattr(position_choice, 'skill_tag'):
                if position_choice.skill_tag == 'Anal':
                    if mc.recently_orgasmed == True and person.anal_cum >= 1:
                        imagebutton:
                            pos(715, 166)
                            idle "ahegaopeach"
                            action NullAction()
                            tooltip "You flood her bowels with your seed."
                    else:
                        imagebutton:
                            pos(715, 166)
                            idle "yesanal"
                            action NullAction()
                            tooltip "You fuck her ass with your cock."
                else:
                    if person.arousal_perc >= 59 and person.anal_cum<=0:
                        imagebutton:
                            pos(715, 166)
                            idle "yesanal"
                            action NullAction()
                            tooltip "Her "+AnalArousal+""
                    else:
                        if person.anal_cum >0:
                            if person.anal_cum == 1:
                                imagebutton:
                                    pos(715, 166)
                                    idle "handass"
                                    action NullAction()
                                    tooltip "You painted her bowels with your cum."
                            else:
                                imagebutton:
                                    pos(715, 166)
                                    idle "ahegaopeach"
                                    action NullAction()
                                    tooltip "Has "+ str(person.anal_cum) +" doses of your cum \n coating her bowels."
                        else:
                            if person.anal_first == mc.name:
                                imagebutton:
                                    pos(715, 166)
                                    idle "claimedass"
                                    action NullAction()
                                    tooltip "You Claimed this Ass!"
                            else:
                                if person.anal_first !=None:
                                    imagebutton:
                                        pos(715, 166)
                                        idle "knowpeach"
                                        action NullAction()
                                        tooltip "Someone else had this ass before you... CLAIM IT!"
            else:
                if person.arousal_perc >= 59 and person.anal_cum<=0:
                    imagebutton:
                        pos(715, 166)
                        idle "yesanal"
                        action NullAction()
                        tooltip "Her "+AnalArousal+""
                else:
                    if person.anal_cum >0:
                        if person.anal_cum == 1:
                                imagebutton:
                                    pos(715, 166)
                                    idle "handass"
                                    action NullAction()
                                    tooltip "You painted her bowels with your cum."
                        else:
                            imagebutton:
                                pos(715, 166)
                                idle "ahegaopeach"
                                action NullAction()
                                tooltip "Has "+ str(person.anal_cum) +" doses of your cum\n coating her bowels."
                    else:
                        if person.anal_first == mc.name:
                            imagebutton:
                                pos(715, 166)
                                idle "claimedass"
                                action NullAction()
                                tooltip "You Claimed this Ass!"
                        else:
                            if person.anal_first !=None:
                                imagebutton:
                                    pos(715, 166)
                                    idle "knowpeach"
                                    action NullAction()
                                    tooltip "Someone else had this ass before you... CLAIM IT!"
        else:
            if person.arousal_perc >= 59 and person.anal_cum<=0:
                imagebutton:
                    pos(715, 166)
                    idle "yesanal"
                    action NullAction()
                    tooltip "Her "+AnalArousal+""
            else:
                if person.anal_cum >0:
                    if person.anal_cum == 1:
                            imagebutton:
                                pos(715, 166)
                                idle "handass"
                                action NullAction()
                                tooltip "You painted her bowels with your cum."
                    else:
                        imagebutton:
                            pos(715, 166)
                            idle "ahegaopeach"
                            action NullAction()
                            tooltip "Has "+ str(person.anal_cum) +" doses of your cum \n coating her bowels."
                else:
                    if person.anal_first == mc.name:
                        imagebutton:
                            pos(715, 166)
                            idle "claimedass"
                            action NullAction()
                            tooltip "You Claimed this Ass!"
                    else:
                        if person.anal_first !=None:
                            imagebutton:
                                pos(715, 166)
                                idle "knowpeach"
                                action NullAction()
                                tooltip "Someone else had this ass before you... CLAIM IT!"
### Vaginal Virgin Flag
        $ VaginalArousal = ""
        $ dayslastsex = 0
        $ daysince = ""
        if person.hymen == 0 and person.vaginal_virgin <= 1:
            $ VaginalArousal = "You can smell her arousal.\n She is ready to be fucked."
            imagebutton:
                pos(752, 166)
                idle "truevirgin"
                action NullAction()
                tooltip "She looks so innocent and inexperienced."
        elif person.hymen ==1:
            $ VaginalArousal = "MmmmMm I still feel you in me! mmmmm please give me more!!! I need it now!\n*You can really smell her arousal*"
            imagebutton:
                pos(752, 166)
                idle "vaghymen"
                action NullAction()
                tooltip "Freshly claimed woman."
        else:
            if person.vaginal_first == mc.name:
                $ VaginalArousal = "Her pussy is dripping for you.\n*You can really smell her arousal*\nCome take me!"
            else:
                $ VaginalArousal = "Her pussy is dripping down her leg.\n*She is really aroused*"
        if person.has_event_day("last_insemination") and person.days_since_event("last_insemination") < 4:
                if person.days_since_event("last_insemination") > 1:
                    $ dayslastsex = 4 - person.days_since_event("last_insemination") 
                    if dayslastsex == 1:
                        $ daysince = "\nMy womb feels empty!"
                    else:
                        $ daysince = "\nYour sperm in me for "+str(dayslastsex)+" more days!\n Such warm butterflies!"
        #the interactive icons during sex stuff
        if 'position_choice' in globals():
            if hasattr(position_choice, 'skill_tag'):
                if position_choice.skill_tag == 'Vaginal':
                    if mc.recently_orgasmed == True and person.vaginal_cum >= 1:
                        if person.hymen ==1:
                            imagebutton:
                                pos(752, 166)
                                idle "vaghymen"
                                action NullAction()
                                tooltip "You mark her fresh womb with your fertile seed! \n Her virinity mixes with your cum.\nYou have claimed her."
                        else:
                            imagebutton:
                                pos(752, 166)
                                idle "ahegaovag"
                                action NullAction()
                                tooltip "You flood her womb with your seed!"
                    else:
                        imagebutton:
                            pos(752, 166)
                            idle "spreadvag"
                            action NullAction()
                            tooltip "You fuck her juicy pussy with your cock."
                else:
                    if person.arousal_perc >= 59 and person.vaginal_cum<=0:
                        imagebutton:
                            pos(752, 166)
                            idle "spreadvag"
                            action NullAction()
                            tooltip ""+VaginalArousal+""
                    else:
                        if person.vaginal_cum >0:
                            if person.vaginal_cum == 1:
                                if person.hymen ==1:
                                    imagebutton:
                                        pos(752, 166)
                                        idle "vaghymen"
                                        action NullAction()
                                        tooltip "You marked her fresh womb with your seed. \n You have claimed her."
                                else:
                                    imagebutton:
                                        pos(752, 166)
                                        idle "openvag"
                                        action NullAction()
                                        tooltip "She has your seed in her womb."
                            else:
                                imagebutton:
                                    pos(752, 166)
                                    idle "ahegaovag"
                                    action NullAction()
                                    tooltip "Has "+ str(person.vaginal_cum) +" doses of your cum\n swimming in her womb."+daysince
                        else:
                            if person.vaginal_first == mc.name:
                                imagebutton:
                                    pos(752, 166)
                                    idle "claimedvag"
                                    action NullAction()
                                    tooltip "You Claimed this Pussy!"
                            else:
                                if person.vaginal_first !=None:
                                    imagebutton:
                                        pos(752, 166)
                                        idle "knowpeach"
                                        action NullAction()
                                        tooltip "Someone else had this pussy before you... OWN IT!"
            else:
                if person.arousal_perc >= 59 and person.vaginal_cum<=0:
                    imagebutton:
                        pos(752, 166)
                        idle "spreadvag"
                        action NullAction()
                        tooltip ""+VaginalArousal+""
                else:
                    if person.vaginal_cum >0:
                        if person.vaginal_cum == 1:
                            if person.hymen ==1:
                                imagebutton:
                                    pos(752, 166)
                                    idle "vaghymen"
                                    action NullAction()
                                    tooltip "You marked her fresh womb with your seed. \n You have claimed her."
                            else:
                                imagebutton:
                                    pos(752, 166)
                                    idle "openvag"
                                    action NullAction()
                                    tooltip "She has your seed in her womb."
                        else:
                            imagebutton:
                                pos(752, 166)
                                idle "ahegaovag"
                                action NullAction()
                                tooltip "Has "+ str(person.vaginal_cum) +" doses of your cum\n swimming in her womb."+daysince
                    else:
                        if person.vaginal_first == mc.name:
                            imagebutton:
                                pos(752, 166)
                                idle "claimedvag"
                                action NullAction()
                                tooltip "You Claimed this Pussy!"
                        else:
                            if person.vaginal_first !=None:
                                imagebutton:
                                    pos(752, 166)
                                    idle "knowpeach"
                                    action NullAction()
                                    tooltip "Someone else had this pussy before you... OWN IT!"
        else:
            if person.arousal_perc >= 59 and person.vaginal_cum<=0:
                imagebutton:
                    pos(752, 166)
                    idle "spreadvag"
                    action NullAction()
                    tooltip ""+VaginalArousal+""
            else:
                if person.vaginal_cum >0:
                    if person.vaginal_cum == 1:
                        if person.hymen ==1:
                            imagebutton:
                                pos(752, 166)
                                idle "vaghymen"
                                action NullAction()
                                tooltip "You marked her fresh womb with your seed. \n You have claimed her."
                        else:
                            imagebutton:
                                pos(752, 166)
                                idle "openvag"
                                action NullAction()
                                tooltip "She has your seed in her womb."
                    else:
                        imagebutton:
                            pos(752, 166)
                            idle "ahegaovag"
                            action NullAction()
                            tooltip "Has "+ str(person.vaginal_cum) +" doses of your cum \n swimming in her womb."+daysince
                else:
                    if person.vaginal_first == mc.name:
                        imagebutton:
                            pos(752, 166)
                            idle "claimedvag"
                            action NullAction()
                            tooltip "You Claimed this Pussy!"
                    else:
                        if person.vaginal_first !=None:
                            imagebutton:
                                pos(752, 166)
                                idle "knowpeach"
                                action NullAction()
                                tooltip "Someone else had this pussy before you... OWN IT!"
#### Had sex today
        if person.had_sex_today:
            imagebutton:
                pos(789, 166)
                idle "hadsextoday"
                action NullAction()
                tooltip "You had fun with her today."  
#### Tranced
        if person.has_exact_role(very_heavy_trance_role):
            imagebutton:
                pos(826, 166)
                idle "ahegaotrance"
                action NullAction()
                tooltip "In a very deep trance! Good time to train her!"
        else:
            if person.has_exact_role(heavy_trance_role):
                imagebutton:
                    pos(826, 166)
                    idle "heavytrance"
                    action NullAction()
                    tooltip "In a deep trance! Good time to train her!"
            else:
                if person.has_exact_role(trance_role):
                    imagebutton:
                        pos(826, 166)
                        idle "starttrance"
                        action NullAction()
                        tooltip "In a trance! She is open to suggestions!"
        if person.event_triggers_dict.get("trance_training_available", True) == False:
            imagebutton:
                pos(826, 166)
                idle "donetrain"
                action NullAction()
                tooltip "Already Trained her!"
