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
                    Show("story_progress", None, person)
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
                if person.has_role(employee_freeuse_role):
                    idle "doggy_style_marker"
                    tooltip "She is the company free-use slut and can be used anytime."
                else:
                    idle "stocking_marker"
                    tooltip "She is a free-use slut, who loves sex."
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
                tooltip "Has no romantic relations with you."
### Teen Flag
        if person.age<19:
            imagebutton:
                pos(322, 166)
                idle "matureteen"
                action NullAction()
                tooltip "She looks so innocent and inexperienced."
###### Birth Control Status
        $ VTbcst = "knowbirthcontrol"
        $ VTbctt = "Don't know if she is on birth control... maybe ask?"
        if person.bc_status_known:
            if person.on_birth_control:
                $ VTbcst = "birthcontrol"
                $ VTbctt = "She is on birth control."
            else:
                $ VTbcst = "nobirthcontrol"
                $ VTbctt = "She is on birth control."
        else:
            $ VTbcst = "knowbirthcontrol"
            $ VTbctt = "Don't know if she is on birth control... maybe ask?"

        imagebutton:
            pos(359, 166)
            idle VTbcst
            action NullAction()
            tooltip VTbctt
        if person.bc_status_known and person.is_highly_fertile and perk_system.has_ability_perk("Ovulation Cycle Perception"):
            imagebutton:
                pos(359, 166)
                idle "beezee"
                action NullAction()
                tooltip "She is not on birth control and highly fertile."
####### Wants Condom
        $ VTcondomst = "knowcondom"
        $ VTcondomtt = "Does she like bareback sex?"
        if person.sexy_opinions.get("bareback sex")==None:
            $ VTcondomst = "knowcondom"
            $ VTcondomtt = "Does she like bareback sex?"
        else:
            if person.sexy_opinions.get("bareback sex")[1]==True:
                if person.opinion.bareback_sex >= 2 and person.wants_creampie and person.has_cum_fetish and person.has_anal_fetish and person.has_breeding_fetish and person.wants_condom()==False:
                    $ VTcondomst = "ahegaocondom"
                    $ VTcondomtt = "She loves it raw!"
                else:
                    if person.opinion.bareback_sex >= 2 and person.wants_condom()==False:
                        $ VTcondomst = "nocondom"
                        $ VTcondomtt = "She seems to love raw sex! "
                        if person.has_anal_fetish==False:
                            $ VTcondomtt += f"\n{{image=ahegaoanal_small}} Needs the Anal Fetish Unlocked." 
                        if person.has_breeding_fetish==False:
                            $ VTcondomtt += f"\n{{image=ahegaovag_small}} Needs the Breeding Fetish Unlocked."
                        if person.has_cum_fetish==False:
                            $ VTcondomtt += f"\n{{image=ahegaomouth_small}} Needs the Cum Fetish Unlocked."
                    else:
                        if person.opinion.bareback_sex >0:
                            $ VTcondomst = "wearcondom"
                            $ VTcondomtt = "Open her mind up to the possibility of more!"
                            $ VTcondomtt += f"\n{{image=question_mark_small}} Make her love raw sex more!"
                        else:
                            if person.opinion.bareback_sex == 0:
                                $ VTcondomst = "wearcondom"
                                $ VTcondomtt = "She's indifferent to raw sex, so make her like it..."
                            else:
                                $ VTcondomst = "nocondom"
                                $ VTcondomtt = "She's indifferent to raw sex, so make her like it..."
                                if person.opinion.bareback_sex == -2:
                                    $ VTcondomtt = "She hates raw sex!"
                                if person.opinion.bareback_sex == -1:
                                    $ VTcondomtt = "She dislikes raw sex!"
            else:
                $ VTcondomst = "knowcondom"
                $ VTcondomtt = "Does she like bareback sex?"

        imagebutton:
            pos(396, 166)
            idle VTcondomst
            action NullAction()
            tooltip VTcondomtt                    
        if person.sexy_opinions.get("bareback sex")!=None:
            if person.opinion.bareback_sex <0 and person.sexy_opinions.get("bareback sex")[1]==True:
                imagebutton:
                    pos(396, 166)
                    idle "dislike"
                    action NullAction()
                    tooltip VTcondomtt
###### Threesome Flag - note polyamorous added
        $ VTpolyst = "knowthreesome"
        $ VTpolytt = "Does she like threesomes?"
        if person.sexy_opinions.get("threesomes")==None:
            $ VTpolyst = "knowthreesome"
            $ VTpolytt = "Does she like threesomes?"
        else:
            if person.sexy_opinions.get("threesomes")[1]==True:
                if person.opinion.threesomes >=2 and person.has_cum_fetish and person.has_anal_fetish and person.opinion.polyamory >=2:
                    $ VTpolyst = "ahegaothreesomes"
                    $ VTpolytt = "More the merrier! The mess we will make!"
                else:
                    if person.opinion.threesomes >=2:
                        $ VTpolyst = "threesometriad"
                        $ VTpolytt = "Open her mind up to more!"
                        if person.has_role(harem_role)==False:
                            if person.love <80:
                                $ VTpolytt += "\n{{image=question_mark_small}} Needs more loving to be added to your polycule!"
                            if person.opinion.polyamory <2:
                                if person.opinion.polyamory ==1:
                                    $ VTpolytt += f"\n{{image=question_mark_small}} Needs to love polyamorous more!"
                                else:
                                    if person.sexy_opinions.get("polyamorous")==None:
                                        $ VTpolytt += f"\n{{image=question_mark_small}} Needs to like polyamorous relationships."
                            else:
                                $ VTpolytt += "\nShe is ready to be part of your polycule!"
                        if person.has_anal_fetish==False:
                            $ VTpolytt += f"\n{{image=ahegaoanal_small}} Needs the Anal Fetish Unlocked." 
                        if person.has_cum_fetish==False:
                            $ VTpolytt += f"\n{{image=ahegaomouth_small}} Needs the Cum Fetish Unlocked."
                    else:
                        if person.opinion.threesomes >0:
                            $ VTpolyst = "opentriad"
                            $ VTpolytt = "Open her mind up to the possibility of more!"
                            $ VTpolytt += f"\n{{image=question_mark_small}} Make her love threesomes!"
                        else:
                            if person.opinion.threesomes == 0:
                                $ VTpolyst = "opentriad"
                                $ VTpolytt = "She's indifferent to threesomes, so make her like it..."
                            else:
                                $ VTpolyst = "opentriad"
                                if person.opinion.threesomes == -2:
                                    $ VTpolytt = f"She hates threesomes!"
                                if person.opinion.threesomes == -1:
                                    $ VTpolytt = f"She dislikes threesomes!"
            else:
                $ VTpolyst = "knowthreesome"
                $ VTpolytt = "Does she like threesomes?"

        imagebutton:
            pos(433, 166)
            idle VTpolyst
            action NullAction()
            tooltip VTpolytt
        if person.sexy_opinions.get("threesomes")!=None:
            if person.sexy_opinions.get("threesomes")[1]==True:
                if person.opinion.threesomes <0 or person.opinion.polyamory <0:
                    imagebutton:
                        pos(433, 166)
                        idle "dislike"
                        action NullAction()
                        tooltip VTpolytt
##### Wants Creampies
        $ VTcreampiest = "knowpeach"
        $ VTcreampiett = "Don't know if she likes creampies, ask her?"
        if person.wants_creampie and person.known_opinion("creampies") and person.known_opinion("anal_creampies") and (person.has_anal_fetish and person.has_breeding_fetish) and (person.opinion.anal_creampies >= 2 and person.known_opinion("anal creampies")) and (person.opinion.creampies >= 2 and person.known_opinion("creampies")):
            $ VTcreampiest = "ahegaopeach"
            $ VTcreampiett = "She wants to be filled!"
        else:
            if (person.opinion.anal_creampies >= 1 and person.known_opinion("anal creampies")) or (person.opinion.creampies >= 1 and person.known_opinion("creampies")):
                $ VTcreampiest = "openpeach"
                $ VTcreampiett = "Keep giving her the cream fillings!"
                if person.known_opinion("anal creampies")==False or person.opinion.anal_creampies < 2:
                    $ VTcreampiett += f"\n{{image=question_mark_small}} Make her love anal creampies!"
                if person.known_opinion("creampies")==False or person.opinion.creampies < 2:
                    $ VTcreampiett += f"\n{{image=question_mark_small}} Make her love vaginal creampies!"
                if person.has_anal_fetish==False:
                    $ VTcreampiett += f"\n{{image=ahegaoanal_small}} Needs the Anal Fetish Unlocked." 
                if person.has_breeding_fetish==False:
                    $ VTcreampiett += f"\n{{image=ahegaovag_small}} Needs the Breeding Fetish Unlocked."
            else:
                if person.known_opinion("anal creampies") or person.known_opinion("creampies"):
                    if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 1) or (person.known_opinion("creampies") and person.opinion.creampies <1):
                        $ VTcreampiest = "yespeach"
                        $ VTcreampiett = "Doesn't seem to like creampies?"
                        if person.known_opinion("anal creampies")==False or person.opinion.anal_creampies < 2:
                            $ VTcreampiett += f"\n{{image=question_mark_small}} Make her like anal creampies!"
                        if person.known_opinion("creampies")==False or person.opinion.creampies < 2:
                            $ VTcreampiett += f"\n{{image=question_mark_small}} Make her like vaginal creampies!"
                    if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 0) or (person.known_opinion("creampies") and person.opinion.creampies <0):
                        $ VTcreampiest = "yespeach"
                        $ VTcreampiett = "She hates creampies!"
                        if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 1):
                            $ VTcreampiett = f"She hates anal creampies!"
                        if (person.known_opinion("creampies") and person.opinion.creampies <1):
                            $ VTcreampiett = f"She hates vaginal creampies!"
                        if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 1) and (person.known_opinion("creampies") and person.opinion.creampies <1):
                            $ VTcreampiett = f"She hates creampies!"
                else:
                    $ VTcreampiest = "knowpeach"
                    $ VTcreampiett = "Don't know if she likes creampies, ask her?"
        imagebutton:
            pos(470, 166)
            idle VTcreampiest
            action NullAction()
            tooltip VTcreampiett                    
        if (person.known_opinion("anal creampies") and person.opinion.anal_creampies < 0) or (person.known_opinion("creampies") and person.opinion.creampies <0):
            imagebutton:
                pos(470, 166)
                idle "dislike"
                action NullAction()
                tooltip VTcreampiett
###### Cum Fetish
        $ VTcumfetishst = "knowlips"
        $ VTcumfetishtt = "Does she like giving blow jobs?"
        if person.sexy_opinions.get("giving blowjobs")==None:
            $ VTcumfetishst = "knowlips"
            $ VTcumfetishtt = "Does she like giving blow jobs?"
        else:
            if person.sexy_opinions.get("giving blowjobs")[1]==True:
                if person.has_cum_fetish:
                    $ VTcumfetishst = "ahegaomouth"
                    $ VTcumfetishtt = "Paint me! Fill me! Feed me! More cummies!"
                else:
                    if person.oral_sex_skill >= 5 and person.opinion.giving_blowjobs >= 2 and (person.opinion.drinking_cum >= 2 or person.opinion.cum_facials >= 2):
                        $ VTcumfetishst = "openmouth"
                        $ VTcumfetishtt = "Loves your cum!"
                        if person.cum_exposure_count<19:
                            $ VTcumfetishtt += f"\n{{image=question_mark_small}} Feed her, spray her, or fill her with your cum \n"+ str(19 - person.cum_exposure_count)+" more times!" 
                        else:
                            $ VTcumfetishtt += "\nWait for the event to trigger!"
                    else:
                        if person.opinion.giving_blowjobs >= 2 and ((person.opinion.drinking_cum >= 2 and person.known_opinion("drinking cum")) or (person.opinion.cum_facials >= 2 and person.known_opinion("cum facials"))):
                            $ VTcumfetishst = "bitelip"
                            $ VTcumfetishtt = "Train her oral skills to vacuum and polish you like a pro!"
                            if person.oral_sex_skill<5:
                                $ VTcumfetishtt += f"\n{{image=question_mark_small}} Train her oral skills "+ str(5 - person.oral_sex_skill)+" more times!\nIncrease her Hoover Power!"
                        else:
                            if person.opinion.giving_blowjobs >= 1:
                                $ VTcumfetishst = "pinklips"
                                $ VTcumfetishtt = "Make her become your cum Queen!"
                                if person.known_opinion("drinking cum")==False:
                                    $ VTcumfetishtt += f"\n{{image=question_mark_small}} Needs her opinion on drinking cum."
                                if person.known_opinion("cum facials")==False:
                                    $ VTcumfetishtt += f"\n{{image=question_mark_small}} Needs her opinion on cum facials."
                                if person.opinion.giving_blowjobs < 2:
                                    $ VTcumfetishtt += f"\n{{image=question_mark_small}} Need her to love giving blowjobs."
                                if person.opinion.drinking_cum < 2:
                                    $ VTcumfetishtt += f"\n{{image=question_mark_small}} Need her to love drinking cum."
                                if person.opinion.cum_facials < 2:
                                    $ VTcumfetishtt += f"\n{{image=question_mark_small}} Need her to love cum facials."
                            else:
                                if person.opinion.giving_blowjobs == 0:
                                    $ VTcumfetishst = "openmouth"
                                    $ VTcumfetishtt = "She's indifferent to oral, so make her like it..."
                                else:
                                    $ VTcumfetishst = "openmouth"
                                    if person.opinion.giving_blowjobs == -2:
                                        $ VTcumfetishtt += f"She hates oral!"
                                    if person.opinion.giving_blowjobs == -1:
                                        $ VTcumfetishtt += f"She dislikes oral!"
            else:
                $ VTcumfetishst = "knowlips"
                $ VTcumfetishtt = "Does she like giving blow jobs?"

        imagebutton:
            pos(507, 166)
            idle VTcumfetishst
            action NullAction()
            tooltip VTcumfetishtt
        if person.sexy_opinions.get("giving blowjobs")!=None:
            if person.opinion.giving_blowjobs < 0 and person.sexy_opinions.get("giving blowjobs")[1]==True:
                imagebutton:
                    pos(507, 166)
                    idle "dislike"
                    action NullAction()
                    tooltip VTcumfetishtt
###### Anal Fetish anal_sex_skill >= 5 .anal_sex_count > 19 or self.anal_creampie_count > 19
        $ VTanalfetishst = "knowpeach"
        $ VTanalfetishtt = "What is her thoughts on anal sex?"
        if person.sexy_opinions.get("anal sex")==None:
            $ VTanalfetishst = "knowpeach"
            $ VTanalfetishtt = "What is her thoughts on anal sex?"
        else:
            if person.sexy_opinions.get("anal sex")[1]==True:
                if person.has_anal_fetish:
                    $ VTanalfetishst = "ahegaopeach"
                    $ VTanalfetishtt = "mmmm stick your cock in my ass!"
                else:
                    if person.anal_sex_skill >= 5 and (person.opinion.anal_sex >= 2  or person.opinion.anal_creampies >= 2):
                        $ VTanalfetishst = "handass"
                        $ VTanalfetishtt = "Sodomize your Anal Queen!"
                        if (person.anal_sex_count<20 or person.anal_creampie_count<20):
                            $ VTanalfetishtt += "\nFill her bowels full of cum "+str(19 - person.anal_creampie_count)+" more times!\nHave anal sex with her "+str(19 - person.anal_sex_count)+" more times!"
                        if (person.anal_sex_count==20 or person.anal_creampie_count==20):
                            $ VTanalfetishtt += "\nWait for the event to trigger!"
                    else:
                        if (person.opinion.anal_creampies >= 1 and person.known_opinion("anal creampies")) or person.opinion.anal_sex >= 1:
                            $ VTanalfetishst = "yesanal"
                            $ VTanalfetishtt = "Train her into your Anal Queen!"
                            if person.anal_sex_skill <5:
                                $ VTanalfetishtt += f"\n{{image=question_mark_small}} Train her anal sex skill "+ str(5 - person.anal_sex_skill)+" more times!"
                            if person.known_opinion("anal creampies")==False:
                                $ VTanalfetishtt += f"\n{{image=question_mark_small}} Need her opinion on anal creampies."
                            if person.opinion.anal_creampies <2:
                                $ VTanalfetishtt += f"\n{{image=question_mark_small}} Need her to love anal creampies."
                            if person.opinion.anal_sex <2:
                                $ VTanalfetishtt += f"\n{{image=question_mark_small}} Need her to love anal sex."
                        else:
                            if person.opinion.anal_sex == 0:
                                $ VTanalfetishst = "bodyconcealed"
                                $ VTanalfetishtt = "She's indifferent to public sex, so make her like it..."
                            else:
                                $ VTanalfetishst = "yespeach"
                                $ VTanalfetishtt = "Sodomize your Anal Queen!"
                                if person.opinion.anal_sex == -2:
                                    $ VTanalfetishtt = f"She hates anal!"
                                if person.opinion.anal_sex == -1:
                                    $ VTanalfetishtt = f"She dislikes anal!"
            else:
                $ VTanalfetishst = "knowpeach"
                $ VTanalfetishtt = "What is her thoughts on anal sex?"

        imagebutton:
            pos(544, 166)
            idle VTanalfetishst
            action NullAction()
            tooltip VTanalfetishtt
        if person.sexy_opinions.get("anal sex")!=None:
            if person.opinion.anal_sex < 0 and person.sexy_opinions.get("anal sex")[1]==True:
                imagebutton:
                    pos(544, 166)
                    idle "dislike"
                    action NullAction()
                    tooltip VTanalfetishtt
###### Breeding Fetish
        $ VTbreedfetishst = "knowpeach"
        $ VTbreedfetishtt = "Does she like vaginal sex?"
        if person.sexy_opinions.get("vaginal sex")==None:
            $ VTbreedfetishst = "knowpeach"
            $ VTbreedfetishtt = "Does she like vaginal sex?"
        else:
            if person.sexy_opinions.get("vaginal sex")[1]==True:
                if person.has_breeding_fetish:
                    $ VTbreedfetishst = "ahegaovag"
                    $ VTbreedfetishtt = "Breed me! I need your cum!"
                else:
                    if person.vaginal_sex_skill >= 5 and person.opinion.vaginal_sex >= 2  and person.opinion.creampies >= 2 and person.known_opinion("creampies"):
                        $ VTbreedfetishst = "openvag"
                        $ VTbreedfetishtt = "She loves your cum!"
                        if person.vaginal_creampie_count<20:
                            $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Fill her full of cum "+ str(20 - person.vaginal_creampie_count)+" more times!"
                        else:
                            $ VTbreedfetishtt += "\nWait for the event to trigger!"
                    else:
                        if person.opinion.vaginal_sex >= 2  and (person.opinion.creampies >= 2 and person.known_opinion("creampies")):
                            $ VTbreedfetishst = "spreadvag"
                            $ VTbreedfetishtt = "Train her vaginal sex skills!"
                            if person.vaginal_sex_skill <5:
                                $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Train her vaginal sex skill "+ str(5 - person.vaginal_sex_skill)+" more times!"
                            if person.opinion.creampies <2:
                                $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Need her to love vaginal creampies."
                        else:            
                            if (person.opinion.creampies >= 1 and person.known_opinion("creampies")) or person.opinion.vaginal_sex >= 1:
                                $ VTbreedfetishst = "vagclosed"
                                $ VTbreedfetishtt = "Train her into your Breeding Stock!"
                                if person.known_opinion("creampies")==False:
                                    $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Need her opinion on vaginal creampies."
                                if person.known_opinion("vaginal sex")==False:
                                    $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Need her opinion on vaginal sex."
                                if person.vaginal_sex_skill <2:
                                    $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Needs her vaginal sex skill raised to 2."
                                if person.opinion.vaginal_sex < 2:
                                    $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Need her opinion on vaginal sex to be positive."
                                if person.opinion.creampies < 2:
                                    $ VTbreedfetishtt += f"\n{{image=question_mark_small}} Need her opinion on vaginal creampies to be positive."
                            else:
                                if person.opinion.vaginal_sex == 0:
                                    $ VTbreedfetishst = "vagclosed"
                                    $ VTbreedfetishtt = "She's indifferent to vaginal sex, so make her like it..."
                                else:
                                    $ VTbreedfetishst = "vagclosed"
                                    $ VTbreedfetishtt = "She's indifferent to vaginal sex, so make her like it..."
                                    if person.opinion.vaginal_sex == -2:
                                        $ VTbreedfetishtt = f"She hates vaginal sex!"
                                    if person.opinion.vaginal_sex == -1:
                                        $ VTbreedfetishtt = f"She dislikes vaginal sex!"
            else:
                $ VTbreedfetishst = "knowpeach"
                $ VTbreedfetishtt = "Does she like vaginal sex?"

        imagebutton:
            pos(581, 166)
            idle VTbreedfetishst
            action NullAction()
            tooltip VTbreedfetishtt
        if person.sexy_opinions.get("vaginal sex")!=None:
            if person.opinion.vaginal_sex < 0 and person.sexy_opinions.get("vaginal sex")[1]==True:
                imagebutton:
                    pos(581, 166)
                    idle "dislike"
                    action NullAction()
                    tooltip VTbreedfetishtt
######## Exhibitionist Fetish
        $ VTexhibitfetishst = "knowbody"
        $ VTexhibitfetishtt = "Does she like public sex?"
        if person.sexy_opinions.get("public sex")==None:
            $ VTexhibitfetishst = "knowbody"
            $ VTexhibitfetishtt = "Does she like public sex?"
        else:
            if person.sexy_opinions.get("public sex")[1]==True:
                if person.opinion.public_sex >=2 and person.opinion.not_wearing_underwear >= 2 and person.opinion.not_wearing_anything >= 2  and person.known_opinion("not wearing underwear") and person.known_opinion("not wearing anything") and person.opinion.showing_her_ass >= 2 and person.opinion.showing_her_tits >= 2  and person.known_opinion("showing her ass") and person.known_opinion("showing her tits") and person.opinion.skimpy_outfits >= 2 and person.opinion.skimpy_uniforms >= 2 and person.known_opinion("skimpy outfits") and person.known_opinion("skimpy uniforms"):
                    $ VTexhibitfetishst = "ahegaoex"
                    $ VTexhibitfetishtt = "My skin needs to breathe and be free!"
                else:
                    if person.opinion.not_wearing_underwear >= 2 and person.opinion.not_wearing_anything >= 2  and person.known_opinion("not wearing underwear") and person.known_opinion("not wearing anything") and person.opinion.skimpy_outfits >= 2 and person.opinion.skimpy_uniforms >= 2 and person.known_opinion("skimpy outfits") and person.known_opinion("skimpy uniforms"):
                        $ VTexhibitfetishst = "nudebody"
                        $ VTexhibitfetishtt = "Needs to be comfortable having sex in public!"
                        if person.opinion.public_sex <2:
                            $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Needs to be more comfortable having public sex."
                        if person.known_opinion("showing her ass")==False:
                            $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know her opinion on showing her ass."
                        if person.known_opinion("showing her tits")==False:
                            $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know her opinion on showing her tits."
                        if person.opinion.showing_her_ass <2:
                            $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Needs to be more comfortable showing her ass." 
                        if person.opinion.showing_her_tits <2:
                            $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Needs to be more comfortable showing her tits."
                    else:
                        if person.opinion.skimpy_outfits >= 2 and person.opinion.skimpy_uniforms >= 2 and person.known_opinion("skimpy outfits") and person.known_opinion("skimpy uniforms"):
                            $ VTexhibitfetishst = "underwear"
                            $ VTexhibitfetishtt = "Train her to be more comfortable not wearing underwear.. How about nothing at all?!"
                            if person.known_opinion("not wearing underwear")==False:
                                $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know her opinion on not wearing underwear."
                            if person.known_opinion("not wearing anything")==False:
                                $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know her opinion on not wearing anything."
                            if person.opinion.not_wearing_underwear <2:
                                $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Needs to be more comfortable wearing no underwear." 
                            if person.opinion.not_wearing_anything <2:
                                $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Needs to be more comfortable not wearing anything."
                        else:
                            if person.opinion.public_sex >0:
                                $ VTexhibitfetishst = "bodyconcealed"
                                $ VTexhibitfetishtt = "She is so shy! Train her into a beautiful Exhibitionist!"
                                if person.known_opinion("skimpy outfits")==False:
                                    $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know her opinion on skimpy outfits."
                                if person.known_opinion("skimpy uniforms")==False:
                                    $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know her opinion on skimpy uniforms."
                                if person.known_opinion("public sex")==False:
                                    $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Need to know if she likes public sex."
                                if person.opinion.skimpy_uniforms <2:
                                    $ VTexhibitfetishtt += f"\n{{image=question_mark_small}} Needs to be more comfortable in skimpy uniforms."
                            else:
                                if person.opinion.public_sex == 0:
                                    $ VTexhibitfetishst = "bodyconcealed"
                                    $ VTexhibitfetishtt = "She's indifferent to public sex, so make her like it..."
                                else:
                                    $ VTexhibitfetishst = "bodyconcealed"
                                    $ VTexhibitfetishtt = "Does she like public sex?"
                                    if person.opinion.public_sex == -2:
                                        $ VTexhibitfetishtt = f"She hates public sex!"
                                    if person.opinion.public_sex == -1:
                                        $ VTexhibitfetishtt = f"She dislikes public sex!"
            else:
                $ VTexhibitfetishst = "knowbody"
                $ VTexhibitfetishtt = "Does she like public sex?"

        imagebutton:
            pos(618, 166)
            idle VTexhibitfetishst
            action NullAction()
            tooltip VTexhibitfetishtt
        if person.sexy_opinions.get("public sex")!=None:
            if person.opinion.public_sex < 0 and person.sexy_opinions.get("public sex")[1]==True:
                imagebutton:
                    pos(618, 166)
                    idle "dislike"
                    action NullAction()
                    tooltip VTexhibitfetishtt
#hymen is 0 = sealed, 1=recently torn bleeding, 2=normal - serum to regenerate vaginal and hymen
#0=virgin, 1=just the tip, 2=full penetration, 3-10 is degree of tightness
### Oral Virgin Flag
        $ VToralst = "truevirgin"
        $ VToraltt = "Her lips seem to beckon you..."
        $ VToralat = "talking"
        if person.oral_virgin == 0:
            $ VToralst = "truevirgin"
            $ VToraltt = "She looks at you with lust \n in her innocent hungry eyes."
            imagebutton:
                pos(678, 166)
                idle VToralst
                action NullAction()
                tooltip VToraltt
        #the interactive icons during sex stuff
        if 'position_choice' in globals():
            if hasattr(position_choice, 'skill_tag'):
                if position_choice.skill_tag == 'Oral':
                    if mc.recently_orgasmed == True and person.oral_cum >=1:
                        $ VToralat = "cuminmouth"
                        $ VToralst = "ahegaomouth"
                        $ VToraltt = "You flood her belly with your cum."
                    else:
                        $ VToralat = "sucking"
                        $ VToralst = "openmouth"
                        $ VToraltt = "You fuck her mouth with your cock."
                else:
                    if hasattr(position_choice, 'name'):
                        if position_choice.name == 'Kissing':
                            $ VToralat = "kissing"
                            $ VToralst = "pinklips"
                            $ VToraltt = "In the throes of kissing you."

        if person.arousal_perc >= 59 and person.oral_cum<=0 and VToralat=="talking":
            $ VToralst = "ahegaoface"
            if person.oral_first == mc.name:
                $ VToraltt = "She starts to drool \n and undress you with her eyes."
            else:
                $ VToraltt = "She looks at you with savage lust in her eyes."
        else:
            if person.oral_cum >0:
                if person.oral_cum == 1:
                        $ VToralst = "ahegaomouth"
                        $ VToraltt = "She has a dose of your protein in her belly."
                else:
                    $ VToralst = "ahegaoface"
                    $ VToraltt = "Has "+ str(person.oral_cum) +" doses of your cum \n swimming in her belly."
            else:
                if person.oral_first == mc.name:
                    $ VToralst = "claimedmouth"
                    $ VToraltt = "You Claimed this Pie Hole!"
                else:
                    if person.oral_first !=None and person.oral_virgin>0:
                        $ VToralst = "knowlips"
                        $ VToraltt = "Someone else had her lips before you... CLAIM IT!"
        imagebutton:
            pos(678, 166)
            idle VToralst
            action NullAction()
            tooltip VToraltt
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
                    if person.anal_first !=None and person.anal_virgin>0:
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
                    if person.vaginal_first !=None and person.hymen==2:
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
