from __future__ import annotations
import renpy
from renpy.display import im
from renpy.display.im import Image
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -100 python:
"""
def get_file_handle(file_name: str) -> str | None:
    return next((x for x in renpy.exports.list_files() if file_name in x), None)

mod_image = Image(get_file_handle("LR2Mod_idle.png"))
mod_hover_image = Image(get_file_handle("LR2Mod_hover.png"))

info_frame_image = Image(get_file_handle("Info_Frame_1.png"))
goal_frame_image = Image(get_file_handle("Goal_Frame_1.png"))

phone_background = im.Scale(Image(get_file_handle("LR2_Phone_Text_Dark.png")), 460, 920)
text_bubble_blue = Image(get_file_handle("LR2_Text_Bubble_Blue.png"))
text_bubble_gray = Image(get_file_handle("LR2_Text_Bubble_Gray.png"))
text_bubble_yellow = Image(get_file_handle("LR2_Text_Bubble_Yellow.png"))

portrait_mask_image = Image(get_file_handle("portrait_mask.png"))
empty_image = Image(get_file_handle("empty_holder.png"))

paper_background_image = Image(get_file_handle("Paper_Background.png"))
science_menu_background_image = Image(get_file_handle("Science_Menu_Background.png"))
map_background_image = Image(get_file_handle("map_background_sketch.png"))
IT_background_image = Image(get_file_handle("IT_Background.png"))

serum_slot_full_image = Image(get_file_handle("Serum_Slot_Full.png"))
serum_slot_empty_image = Image(get_file_handle("Serum_Slot_Empty.png"))
serum_slot_incorrect_image = Image(get_file_handle("Serum_Slot_Incorrect.png"))

#Harem/girlfriend/affair
empty_token_small_image = im.Scale(Image(get_file_handle("empty_token.png")), 18, 18)
renpy.image("empty_token_small", empty_token_small_image)

gf_token_small_image = im.Scale(Image(get_file_handle("girlfriend.png")), 18, 18)
renpy.image("gf_token_small", gf_token_small_image)

paramour_token_small_image = im.Scale(Image(get_file_handle("paramour.png")), 18, 18)
renpy.image("paramour_token_small", paramour_token_small_image)

parapoly_token_small_image = im.Scale(Image(get_file_handle("parapoly32.png")), 18, 18)
renpy.image("parapoly_token_small", parapoly_token_small_image)

full_star_token_small_image = im.Scale(Image(get_file_handle("favourite_star_filled.png")), 18, 18)
renpy.image("full_star_token_small", full_star_token_small_image)

empty_star_token_small_image = im.Scale(Image(get_file_handle("favourite_star_empty.png")), 18, 18)
renpy.image("empty_star_token_small", empty_star_token_small_image)

harem_token_small_image = im.Scale(Image(get_file_handle("harem.png")), 18, 18)
renpy.image("harem_token_small", harem_token_small_image)

# scaled images
taboo_break_image = im.Scale(Image(get_file_handle("taboo_lock_alt.png")), 16, 22)
renpy.image("taboo_break", taboo_break_image)
thumbs_up_image = im.Scale(Image(get_file_handle("thumbs_up_small.png")), 16, 22)
renpy.image("thumbs_up", thumbs_up_image)
thumbs_down_image = im.Scale(Image(get_file_handle("thumbs_down_small.png")), 16, 22)
renpy.image("thumbs_down", thumbs_down_image)

energy_token_small_image = im.Scale(Image(get_file_handle("energy_token.png")), 18, 18)
renpy.image("energy_token_small", energy_token_small_image)

arousal_token_small_image = im.Scale(Image(get_file_handle("arousal_token.png")), 18, 18)
renpy.image("arousal_token_small", arousal_token_small_image)

red_heart_token_small_image = im.Scale(Image(get_file_handle("heart/red_heart.png")), 18, 18)
renpy.image("red_heart_token_small", red_heart_token_small_image)

gold_heart_token_small_image = im.Scale(Image(get_file_handle("heart/gold_heart.png")), 18, 18)
renpy.image("gold_heart_token_small", gold_heart_token_small_image)

lust_eye_token_small_image = im.Scale(Image(get_file_handle("lust_eye.png")), 18, 18)
renpy.image("lust_eye_token_small", lust_eye_token_small_image)

feeding_bottle_token_small_image = im.Scale(Image(get_file_handle("feeding_bottle.png")), 18, 18)
renpy.image("feeding_bottle_token_small", feeding_bottle_token_small_image)

fertile_token_small_image = im.Scale(Image(get_file_handle("fertile_token.png")), 18, 18)
renpy.image("fertile_token_small", fertile_token_small_image)

hadsex_token_small_image = im.Scale(Image(get_file_handle("hadsex_token.png")), 18, 18)
renpy.image("hadsex_token_small", hadsex_token_small_image)

happy_small_image = im.Scale(Image(get_file_handle("happy.png")), 18, 18)
renpy.image("happy_token_small", happy_small_image)

underwear_small_image = im.Scale(Image(get_file_handle("underwear_token.png")), 18, 18)
renpy.image("underwear_token_small", underwear_small_image)

padlock_small_image = im.Scale(Image(get_file_handle("padlock.png")), 18, 18)
renpy.image("padlock_token_small", padlock_small_image)

triskelion_small_image = im.Scale(Image(get_file_handle("triskelion.png")), 18, 18)
renpy.image("triskelion_token_small", triskelion_small_image)

question_mark_small_image = im.Scale(Image(get_file_handle("question.png")), 18, 18)
renpy.image("question_mark_small", question_mark_small_image)

information_small_image = im.Scale(Image(get_file_handle("information.png")), 18, 18)
renpy.image("information_token_small", information_small_image)

infraction_token_small_image = im.Scale(Image(get_file_handle("infraction_token.png")), 18, 18)
renpy.image("infraction_token_small", infraction_token_small_image)

speech_bubble_small_image = im.Scale(Image(get_file_handle("speech_bubble.png")), 18, 18)
renpy.image("speech_bubble_token_small", speech_bubble_small_image)

speech_bubble_exclamation_small_image = im.Scale(Image(get_file_handle("speech_bubble_exclamation.png")), 18, 18)
renpy.image("speech_bubble_exclamation_token_small", speech_bubble_exclamation_small_image)

phone_token_small_image = im.Scale(Image(get_file_handle("phone_token.png")), 18, 18)
renpy.image("phone_token_small", phone_token_small_image)

vial_token_small_image = im.Scale(Image(get_file_handle("vial.png")), 18, 18)
renpy.image("vial_token_small", vial_token_small_image)

vial2_token_small_image = im.Scale(Image(get_file_handle("vial2.png")), 18, 18)
renpy.image("vial2_token_small", vial2_token_small_image)

vial3_token_small_image = im.Scale(Image(get_file_handle("vial3.png")), 18, 18)
renpy.image("vial3_token_small", vial3_token_small_image)

virgin_token_small_image = im.Scale(Image(get_file_handle("virgin.png")), 18, 18)
renpy.image("virgin_token_small", virgin_token_small_image)

dna_token_small_image = im.Scale(Image(get_file_handle("dna.png")), 18, 18)
renpy.image("dna_token_small", dna_token_small_image)

progress_token_small_image = im.Scale(Image(get_file_handle("Progress32.png")), 18, 18)
renpy.image("progress_token_small", progress_token_small_image)

stocking_token_small_image = im.Scale(Image(get_file_handle("stocking_token.png")), 18, 18)
renpy.image("stocking_token_small", stocking_token_small_image)

drop_down_token_image = Image(get_file_handle("drop_down_token.png")) # size 24 x 24
renpy.image("dropdown_token", drop_down_token_image)

matureteen_token_small_image = im.Scale(Image(get_file_handle("matureteen.png")), 18, 18)
renpy.image("matureteen_token_small", matureteen_token_small_image)

beezee_token_small_image = im.Scale(Image(get_file_handle("beezee.png")), 18, 18)
renpy.image("beezee_token_small", beezee_token_small_image)

vial_image = Image(get_file_handle("vial.png"))
vial2_image = Image(get_file_handle("vial2.png"))
vial3_image = Image(get_file_handle("vial3.png"))
dna_image = Image(get_file_handle("dna.png"))
question_image = Image(get_file_handle("question.png"))
home_image = Image(get_file_handle("home_marker.png"))
feeding_bottle_image = Image(get_file_handle("feeding_bottle.png"))
fertile_image = Image(get_file_handle("fertile_token.png"))
stocking_image = Image(get_file_handle("stocking_token.png"))
virgin_image = Image(get_file_handle("virgin_token.png"))
bc_image = Image(get_file_handle("bc_token32.png"))
nobc_image = Image(get_file_handle("nobc_token32.png"))
beezee_image = Image(get_file_handle("beezee.png"))
knowbc_image = Image(get_file_handle("knowbc_token32.png"))
dontknow_image = Image(get_file_handle("dontknow32.png"))
parapoly_image = Image(get_file_handle("parapoly32.png"))
polyamorous_image = Image(get_file_handle("harem32.png"))
paramour_image = Image(get_file_handle("paramour32.png"))
rings_image = Image(get_file_handle("rings32.png"))
girlfriend_image = Image(get_file_handle("girlfriend32.png"))

hadsextoday_image = Image(get_file_handle("sex32.png"))
truevirgin_image = Image(get_file_handle("virgin.png"))
dislike_image = Image(get_file_handle("dislike.png"))
vaghymen_image = Image(get_file_handle("vaghymen.png"))

ahegaocondom_image = Image(get_file_handle("ahegaocondom.png"))
wearcondom_image = Image(get_file_handle("wearcondom.png"))
nocondom_image = Image(get_file_handle("nocondom.png"))
knowcondom_image = Image(get_file_handle("knowcondom.png"))

bareback_image = Image(get_file_handle("bareback.png"))
nocream_image = Image(get_file_handle("nocream.png"))
knowpeach_image = Image(get_file_handle("knowpeach.png"))
openpeach_image = Image(get_file_handle("openpeach.png"))
yespeach_image = Image(get_file_handle("yespeach.png"))

ahegaomouth_image = Image(get_file_handle("ahegaomouth.png"))
openmouth_image = Image(get_file_handle("openmouth.png"))
bitelip_image = Image(get_file_handle("bitelip.png"))
pinklips_image = Image(get_file_handle("pinklips.png"))
knowlips_image = Image(get_file_handle("knowlips.png"))

ahegaopeach_image = Image(get_file_handle("ahegaoanal.png"))
handass_image = Image(get_file_handle("handass.png"))
yesanal_image = Image(get_file_handle("yesanal.png"))

ahegaovag_image = Image(get_file_handle("ahegaovag.png"))
openvag_image = Image(get_file_handle("openvag.png"))
spreadvag_image = Image(get_file_handle("spreadvag.png"))
vagclosed_image = Image(get_file_handle("vagclosed.png"))
knowvag_image = Image(get_file_handle("knowvag.png"))

ahegaoex_image = Image(get_file_handle("ahegaoex.png"))
nudebody_image = Image(get_file_handle("nudebody.png"))
underwear_image = Image(get_file_handle("underwear.png"))
bodyconcealed_image = Image(get_file_handle("bodyconcealed.png"))
knowbody_image = Image(get_file_handle("knowbody.png"))

ahegaothreesomes_image = Image(get_file_handle("ahegaothreesomes.png"))
threesometriad_image = Image(get_file_handle("threesometriad.png"))
opentriad_image = Image(get_file_handle("opentriad.png"))
knowthreesome_image = Image(get_file_handle("knowthreesome.png"))

ahegaotrance_image = Image(get_file_handle("ahegaotrance.png"))
heavytrance_image = Image(get_file_handle("heavytrance.png"))
starttrance_image = Image(get_file_handle("starttrance.png"))
donetrain_image = Image(get_file_handle("donetrain.png"))

ahegaoface_image = Image(get_file_handle("ahegaoface.png"))

ahegaotrance_token_small_image = im.Scale(Image(get_file_handle("ahegaotrance.png")), 18, 18)
renpy.image("ahegaotrance_token_small", ahegaotrance_token_small_image)

heavytrance_token_small_image = im.Scale(Image(get_file_handle("heavytrance.png")), 18, 18)
renpy.image("heavytrance_token_small", heavytrance_token_small_image)

starttrance_token_small_image = im.Scale(Image(get_file_handle("starttrance.png")), 18, 18)
renpy.image("starttrance_token_small", starttrance_token_small_image)

donetrain_token_small_image = im.Scale(Image(get_file_handle("donetrain.png")), 18, 18)
renpy.image("donetrain_token_small", donetrain_token_small_image)

matureteen_image = Image(get_file_handle("matureteen.png"))

claimedmouth_image = Image(get_file_handle("claimedmouth.png"))
claimedass_image = Image(get_file_handle("claimedass.png"))
claimedvag_image = Image(get_file_handle("claimedvag.png"))

ahegaoanal_small_image = im.Scale(Image(get_file_handle("ahegaoanal.png")), 18, 18)
renpy.image("ahegaoanal_small", ahegaoanal_small_image)

ahegaovag_small_image = im.Scale(Image(get_file_handle("ahegaovag.png")), 18, 18)
renpy.image("ahegaovag_small", ahegaovag_small_image)

ahegaomouth_small_image = im.Scale(Image(get_file_handle("ahegaomouth.png")), 18, 18)
renpy.image("ahegaomouth_small", ahegaomouth_small_image)

yesanal_small_image = im.Scale(Image(get_file_handle("yesanal.png")), 18, 18)
renpy.image("yesanal_small", yesanal_small_image)

yespeach_small_image = im.Scale(Image(get_file_handle("yespeach.png")), 18, 18)
renpy.image("yespeach_small", yespeach_small_image)

bareback_small_image = im.Scale(Image(get_file_handle("bareback.png")), 18, 18)
renpy.image("bareback_small", bareback_small_image)