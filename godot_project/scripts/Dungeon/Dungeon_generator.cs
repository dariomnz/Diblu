using Godot;
using System;

namespace Godot
{
    
    [Tool]
    public class Dungeon_generator : TileMap
    {
        
        private bool _generate_new_dungeon = false; 
        [Export]
        public bool Generate_new_dungeon
        { 
            get {
                return _generate_new_dungeon;
                } 
            set {
                generate_dungeon(value);
                }
        }

        
        [Export(PropertyHint.Range,"3,50")]
        private int max_rooms = 10;
        [Export(PropertyHint.Range,"3,50")]
        private int min_rooms = 3;

        [Export]
        private Vector2 wallBorder = new Vector2(60,60);

        private RandomNumberGenerator rand = new RandomNumberGenerator();
        private Godot.Collections.Array<PackedScene> _entrances = new Godot.Collections.Array<PackedScene>(); 
        public Godot.Collections.Array<PackedScene> Entrances {
            get {
            return _entrances; 
            } 
            set => _entrances = value; }


        private Godot.Collections.Array<PackedScene> _rooms = new Godot.Collections.Array<PackedScene>();
        public Godot.Collections.Array<PackedScene> Rooms { get => _rooms; set => _rooms = value; }

        private Godot.Collections.Array<PackedScene> _corridors = new Godot.Collections.Array<PackedScene>();
        public Godot.Collections.Array<PackedScene> Corridors { get => _corridors; set => _corridors = value; }

        private TileMap last_room;

        private Godot.Collections.Array used_rects = new Godot.Collections.Array();

        private Godot.Collections.Array nex_trys = new Godot.Collections.Array();

        private Godot.Collections.Array actual_rooms = new Godot.Collections.Array();

        private Godot.Collections.Array total_rooms = new Godot.Collections.Array();


        // Declare member variables here. Examples:
        // private int a = 2;
        // private string b = "text";

        // Called when the node enters the scene tree for the first time.
        public override void _Ready()
        {
            generate_dungeon(true);

            var packedPlayer = (PackedScene)ResourceLoader.Load("res://prefabs/entity/Slime/Slime.tscn");
            var player = packedPlayer.Instance() as Node2D;
            AddChild(player);
            player.GlobalPosition = new Vector2(100,100);
        }

        public void generate_dungeon(bool newValue)
        {
            if (!newValue)
            {
                return;
            }

            uint startTime = OS.GetTicksMsec();

            // Clear the level
            foreach (Node child in GetChildren())
            {
                if (child.Name != "Walls")
                {
                    child.QueueFree();
                }
            }

            GetNode<TileMap>("Walls").Clear();

            rand.Randomize();

            int num_rooms = rand.RandiRange(min_rooms,max_rooms);
            foreach (var item in GD.Range(num_rooms))
            {
                try_generate_new_room();
            }
            

            foreach (Rect2 itiUsedRect in used_rects)
            {
                Rect2 used_rect = itiUsedRect;
                used_rect.Position = WorldToMap(used_rect.Position)-wallBorder;
                used_rect.Size = WorldToMap(used_rect.Size)+wallBorder*2;
                foreach (int x in GD.Range((int)used_rect.Position.x,(int)(used_rect.Position.x+used_rect.Size.x)))
                {
                    foreach (int y in GD.Range((int)used_rect.Position.y,(int)(used_rect.Position.y+used_rect.Size.y)))
                    {
                        TileMap walls = GetNode<TileMap>("Walls");
                        if (GetCell(x,y-2) != walls.TileSet.FindTileByName("Wall_top"))
                        {
                            // GD.Print(walls);
                            walls.Call("set_cell",x,y,walls.TileSet.FindTileByName("Wall_down"));
                            walls.UpdateBitmaskArea(new Vector2(x,y));
                        }
                    }
                }
            }

            foreach (Node2D room in total_rooms)
            {
                remove_walls(room);
            }

            used_rects.Clear();
            actual_rooms.Clear();
            total_rooms.Clear();

            last_room = null;

            GD.Print("Time to generate ",num_rooms," rooms: ",OS.GetTicksMsec()-startTime," ms");


            
        }

        private void try_generate_new_room()
        {
            bool isGenerate = false;
            Godot.Collections.Array tryed = new Godot.Collections.Array();
            while (!isGenerate)
            {
                Godot.Collections.Array posible_direction = getPosibleDirection();

                var next_direction = (int)posible_direction[rand.RandiRange(0,posible_direction.Count-1)];

                if (actual_rooms.Count != 0)
                {
                    bool is_choose = false;
                    while (!is_choose)
                    {
                        last_room = (TileMap)actual_rooms[rand.RandiRange(0,actual_rooms.Count-1)];

                        if (!tryed.Contains(last_room))
                        {
                            is_choose = true;
                        }
                        else if(tryed.Count != 0)
                        {
                            tryed.Add(last_room);
                        }
                        else if (tryed.Count >= actual_rooms.Count)
                        {
                            tryed.Clear();
                        }
                    }
                }
                if (generateNewRoom(next_direction))
                {
                    isGenerate = true;
                } 
            }

        }

        private bool generateNewRoom(int direction)
        {
            
            if (!getPosibleDirection().Contains(direction))
            {
                return false;
            }

            

            int UP = Global.UP;
            int DOWN = Global.DOWN;
            int LEFT = Global.LEFT;
            int RIGHT = Global.RIGHT;

            int from = Global.DOWN;
            int to = Global.UP;
            bool isHorizontal = true;

            if (direction == UP)
            {
                from = UP;
                to = DOWN;
                isHorizontal = false;
            }
            else if (direction == DOWN)
            {
                from = DOWN;
                to = UP;
                isHorizontal = false;
            }
            else if (direction == LEFT)
            {
                from = LEFT;
                to = RIGHT;
            }
            else if (direction == RIGHT)
            {
                from = RIGHT;
                to = LEFT;
            }
            
            if (last_room == null)
            {
                last_room = (TileMap)newEntrance(this);
            }
            // GD.Print("DSAtqwet");
            
            // GD.Print((Collections.Array)last_room.Get("posible_exits").GetType());
            // var _lastPosibleExits = (Collections.Array)last_room.Get("posible_exits");
            
            Collections.Array lastPosibleExits = (Collections.Array)last_room.Get("posible_exits");
            
            var _lastPosibleExits = (Collections.Array)lastPosibleExits[from];
            if (_lastPosibleExits.Count==0)
            {
                return false;
            }
            // GD.Print(_lastPosibleExits[0].GetType());

            Vector2 outCorridorPosition = (Vector2)_lastPosibleExits[rand.RandiRange(0,_lastPosibleExits.Count-1)];
            
            var corridor = (Node2D)newCorridor(last_room);
            if (isHorizontal)
            {
                corridor.Set("direction",1);
            }
            else
            {
                corridor.Set("direction",2);
            }

            // GD.Print("DSAtqwet");

            outCorridorPosition = MapToWorld(outCorridorPosition)+last_room.GlobalPosition;
            
            var corridorExits = (Collections.Array)corridor.Get("posible_exits");
            var _corridorExitsTo = (Collections.Array)corridorExits[to];
            var _corridorExitsFrom = (Collections.Array)corridorExits[from];

            // GD.Print(_corridorExitsTo.GetType());

            outCorridorPosition -= MapToWorld((Vector2)_corridorExitsTo[0]);

            corridor.GlobalPosition = outCorridorPosition;

            var room = (Node2D)newRoom(corridor);
            var posibleEntrances = (Collections.Array)room.Get("posible_exits");
            var _posibleEntrances = (Collections.Array)posibleEntrances[to];

            room.GlobalPosition = corridor.GlobalPosition +MapToWorld((Vector2)_corridorExitsFrom[0]);

            if (_posibleEntrances.Count == 0)
            {
                room.Free();
                corridor.Free();
                return false;
            }

            var inCorridorPosition = _posibleEntrances[rand.RandiRange(0,_posibleEntrances.Count-1)];

            inCorridorPosition = MapToWorld((Vector2)inCorridorPosition);

            room.GlobalPosition -= (Vector2)inCorridorPosition;

            var roomUsedFloor = (Rect2)room.Get("used_floor");
            foreach (Rect2 usedRect in used_rects)
            {
                if (roomUsedFloor.Intersects(usedRect))
                {
                    room.Free();
                    corridor.Free();
                    return false;
                }
            }

            if (!used_rects.Contains(last_room.Get("used_floor")))
            {
                used_rects.Add(last_room.Get("used_floor"));
            }
            if (!used_rects.Contains(corridor.Get("used_floor")))
            {
                used_rects.Add(corridor.Get("used_floor"));
            }
            if (!used_rects.Contains(room.Get("used_floor")))
            {
                used_rects.Add(room.Get("used_floor"));
            }

            
            if (!actual_rooms.Contains(last_room))
            {
                actual_rooms.Add(last_room);
            }
            if (!actual_rooms.Contains(room))
            {
                actual_rooms.Add(room);
            }


            if (!total_rooms.Contains(last_room))
            {
                total_rooms.Add(last_room);
            }
            if (!total_rooms.Contains(corridor))
            {
                total_rooms.Add(corridor);
            }
            if (!total_rooms.Contains(room))
            {
                total_rooms.Add(room);
            }




            return true;
        }
        private void remove_walls(Node2D room)
        {
            Vector2 roomPosition = WorldToMap(room.GlobalPosition);
            Collections.Array wallsArr = (Collections.Array)room.Call("get_floor_arr");
            foreach (Vector2 wall in wallsArr)
            {
                GetNode<TileMap>("Walls").Call("set_cell",roomPosition.x+wall.x,roomPosition.y+wall.y,GetNode<TileMap>("Walls").TileSet.FindTileByName("Wall_remove"));
            }
        }

        private Node newEntrance(Node2D parent)
        {
            
            var __entrances = getEntrances();
            // GD.Print("asdfadf");
            // GD.Print(__entrances);
            Node entranceInstance = __entrances[rand.RandiRange(0,__entrances.Count-1)].Instance();

            // GD.Print(entranceInstance);
            parent.AddChild(entranceInstance);
            entranceInstance.Call("initialize");
            entranceInstance.Owner = GetParent();
            
            return entranceInstance;    
        }
        private Node newRoom(Node2D parent)
        {
            var __rooms = getRooms();
            Node roomInstance = __rooms[rand.RandiRange(0,__rooms.Count-1)].Instance();

            parent.AddChild(roomInstance);
            roomInstance.Call("initialize");
            roomInstance.Owner = GetParent();

            return roomInstance;
        }

        private Node newCorridor(Node2D parent)
        {
            var __corridors = getCorridors();
            Node corridorInstance = __corridors[rand.RandiRange(0,__corridors.Count-1)].Instance();

            parent.AddChild(corridorInstance);
            corridorInstance.Call("initialize");
            corridorInstance.Owner = GetParent();
            corridorInstance.Call("randomize_length",7);

            return corridorInstance;
        }


        private Collections.Array<PackedScene> getEntrances()
        {
            if (_entrances.Count != 0)
            {
                // GD.Print("_entrances",_entrances);
                return _entrances;
            }
            return getPacketScenes("res://prefabs/Dungeon/Rooms/Entrance/");
        }
        private Collections.Array<PackedScene> getRooms()
        {
            if (_rooms.Count != 0)
            {
                // GD.Print("Rooms",_rooms);
                return _rooms;
            }
            return getPacketScenes("res://prefabs/Dungeon/Rooms/Normal/");
        }



        private Collections.Array<PackedScene> getCorridors()
        {
            if (_corridors.Count != 0)
            {
                // GD.Print("_corridors",_corridors);
                return _corridors;
            }
            return getPacketScenes("res://prefabs/Dungeon/Corridors/");
        }







        private Collections.Array<PackedScene> getPacketScenes(String dirPath)
        {
            Directory directory = new Directory();
            Collections.Array<PackedScene> packedScenes = new Collections.Array<PackedScene>();

            directory.Open(dirPath);
            directory.ListDirBegin();
            while (true)
            {
                String file = directory.GetNext();
                if (file == "")
                {
                    break;
                }
                else if (!file.BeginsWith("."))
                {
                    packedScenes.Add(GD.Load<PackedScene>(dirPath+file));
                }
            }
            // GD.Print(packedScenes);
            return packedScenes;
        }


        private Godot.Collections.Array getPosibleDirection()
        {
            
            Godot.Collections.Array posible_direction = new Godot.Collections.Array();
            posible_direction.Add(0);
            posible_direction.Add(1);
            posible_direction.Add(2);
            posible_direction.Add(3);
            return posible_direction;
        }
    }
}