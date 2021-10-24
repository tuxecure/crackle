
pub trait Config<T> {
    fn new(key: &'static str) -> Self;
    fn add_argument(&self, value: &'static str) -> Self;
    fn update_value(&self, value: T) -> Self;
    fn describe(&self);
}
pub struct Lever {
    key: String,
    value: bool,
}
impl Config<bool> for Lever {
    fn new(key: &'static str) -> Self {
        Lever{
            key: key.to_string(),
            value: false,
        }
    }
    fn describe(&self) {

    }
    fn add_argument(&self, value: &'static str) -> Lever {

        return *self
    }
    fn update_value(&self, value: bool) -> Lever {

        return *self
    }
}

pub struct TextParameter {
    key: String,
    value: String,
}
impl Config<String> for TextParameter {
    fn new(key: &'static str) -> TextParameter { 
        TextParameter{
            key: key.to_string(),
            value: "".to_string(),
        }
    }
    fn describe(&self) {

    }
    fn add_argument(&self, value: &'static str) -> TextParameter {

        return *self
    }
    fn update_value(&self, value: String) -> TextParameter {

        return  *self
    }
}

pub struct NumericParameter {
    key: String,
    value: i32,
}
impl Config<i32> for NumericParameter {
    fn new(key: &'static str) -> NumericParameter { 
        NumericParameter{
            key: key.to_string(),
            value: 0,
        }
    }
    fn describe(&self) {

    }
    fn add_argument(&self, value: &'static str) -> NumericParameter {

        return *self
    }
    fn update_value(&self, value: i32) -> NumericParameter {

        return *self
    }
}
