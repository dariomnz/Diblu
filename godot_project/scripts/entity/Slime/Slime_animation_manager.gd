extends "res://scripts/entity/Animation_manager.gd"

func _ready():
	states_seek={
	"run":["run"],
	"jump":["jump"],
	"attack":["attack"],
	"dash":["dash"]
	}
	
	nodes = {
		"idle":["idle","run","jump","attack","dash"],
		"run":["run","jump","attack","dash"],
		"jump":["jump"],
		"attack":["attack"],
		"dash":["dash"]
	}
	
	travel("idle")

# Override
# Define a donde pasa cuando cambia
func animation_ended(anim_name : String):
	
	anim_name = anim_name.split("_")[0]
	
	if anim_name == "idle":
		travel("idle",true)
	elif anim_name == "run":
		travel("idle",true)
	elif anim_name == "jump":
		travel("idle",true)
	elif anim_name == "attack":
		travel("idle",true)
	elif anim_name == "dash":
		travel("idle",true)


