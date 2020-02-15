use std::collections::HashMap;

pub struct Line {
    inscriptions: HashMap<i32, u32>,
}

pub struct Face {
    lines: HashMap<i32, Line>,
}

pub struct Stele {
    faces: HashMap<i32, Face>,
}

pub struct Tonyukuk {
    steles: HashMap<i32, Stele>,
}
