extends Control

const NONE = 0
const PAUSE = 1
const SETTINGS = 2

const ENTER_TOP = 0
const ENTER_DOWN = 1
const ENTER_LEFT = 2
const ENTER_RIGHT = 3

const EXIT_TOP = 4
const EXIT_DOWN = 5
const EXIT_LEFT = 6
const EXIT_RIGHT = 7

const ENTER = 0
const EXIT = 1
# Declare member variables here. Examples:
# var a = 2
# var b = "text"
var actual_GUI = NONE

onready var controlers = {
	NONE:null,
	PAUSE:get_node("Pause controler"),
	SETTINGS:get_node("Settings")
}
# Tiene todas las GUIS posibles
# dentro de ellas las transiciones posibles
# Y dentro como cambia la que entra y la que sale
var GUIS = {
	NONE:{
		PAUSE:{
			ENTER:ENTER_TOP
			},
	},
	PAUSE:{
		SETTINGS:{
			ENTER:ENTER_RIGHT,
			EXIT:EXIT_LEFT
			},
		NONE:{
			EXIT:EXIT_TOP
			}
	},
	SETTINGS:{
		PAUSE:{
			ENTER:ENTER_LEFT,
			EXIT:EXIT_RIGHT
		},
		NONE:{
			EXIT:EXIT_TOP
			}
	},
}
func _ready():
	var _err = get_tree().get_root().connect("size_changed", self, "change_resolution")
	_err = $Settings.connect("change_debug",self,"change_debug")

#func _process(_delta):
#
#	if Input.is_action_just_pressed("ui_cancel"):
#		if get_tree().paused == true:
#			get_tree().paused = false
#			change_GUI(NONE)
#		else:
#			get_tree().paused = true
#			change_GUI(PAUSE)
		

func change_GUI(newGUI):
	# Comprueba que la actual esta en las GUIS
	if actual_GUI in GUIS:
		# Comprueba que hay controlador y hay transicion
		if newGUI in GUIS[actual_GUI] and newGUI in controlers:
			transition_GUI(actual_GUI,newGUI)
			actual_GUI=newGUI

func transition_GUI(_actual_GUI,newGUI):
	var transitionDict = GUIS[_actual_GUI][newGUI]
	
	for enter_exit in transitionDict.keys():
		match(enter_exit):
			ENTER:
				if controlers[newGUI]:
					match(transitionDict[enter_exit]):
						ENTER_TOP : 
							controlers[newGUI].enter_top()
						ENTER_DOWN :
							controlers[newGUI].enter_down()
						ENTER_LEFT : 
							controlers[newGUI].enter_left()
						ENTER_RIGHT :
							controlers[newGUI].enter_right()
			EXIT:
				if controlers[_actual_GUI]:
					match(transitionDict[enter_exit]):
						EXIT_TOP : 
							controlers[_actual_GUI].exit_top()
						EXIT_DOWN : 
							controlers[_actual_GUI].exit_down()
						EXIT_LEFT : 
							controlers[_actual_GUI].exit_left()
						EXIT_RIGHT : 
							controlers[_actual_GUI].exit_right()
func change_resolution():
	for child in get_children():
		var new_rect = get_viewport_rect().size
		child.set("position_out_left",Vector2(-new_rect.x,0))
		child.set("position_out_right",Vector2(new_rect.x,0))
		child.set("position_out_top",Vector2(0,-new_rect.y))
		child.set("position_out_down",Vector2(0,-new_rect.y))
		
func change_debug(newDebug):
	$GUI.visible = newDebug
	
	var camera = get_tree().get_nodes_in_group("camera")[0]
	if newDebug:
		camera.max_zoom = 100
	else:
		camera.max_zoom = 2
