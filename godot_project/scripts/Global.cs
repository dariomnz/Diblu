using Godot;
using System;

public class Global : Node
{
    
    public Vector2 CHUNKSIZE = new Vector2(16,16);
    public Vector2 TILESIZE = new Vector2(16,16);

    public Vector2 CHUNKAMOUNT = new Vector2(3,2);

    public const int ITEMSTACKLIMIT = 256;

    public Godot.Collections.Dictionary<String,int> POSIBLEFURNITURE = new Godot.Collections.Dictionary<string, int>(){
        {"crate",0},
        {"campfire",1},
    };

    public const int NORMALKNOCKBACK = 200;

    public const int UP = 0;
    public const int DOWN = 1;
    public const int LEFT = 2;
    public const int RIGHT = 3;
    public const int HORIZONTAL = 1;
    public const int VERTICAL = 2;


    public bool isDebug = true;
}
