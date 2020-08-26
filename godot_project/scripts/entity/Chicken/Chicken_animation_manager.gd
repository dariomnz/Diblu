extends "res://scripts/entity/Animation_manager.gd"

func _ready():
	states_seek={
	"run":["run"],
	}
	nodes = {
		"idle":["idle","run","hit"],
		"run":["run","hit"],
		"hit":["hit"],
	}
	
	posible_directions = 2
	
	travel("idle")

# Override
# Define a donde pasa cuando cambia
func animation_ended(anim_name : String):
	
	anim_name = anim_name.split("_")[0]
	
	if anim_name == "idle":
		travel("idle",true)
	elif anim_name == "run":
		travel("idle",true)
	elif anim_name == "hit":
		travel("idle",true)
