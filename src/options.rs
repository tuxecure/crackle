
trait Option<T> {
    fn new(key: &'static str) -> Self;
    fn add_argument(&self, value: String);
    fn update_value(&self, value: T);
    fn describe(&self);
}
pub struct BooleanOpt {
    key: String,
    value: bool,
}
impl Option<bool> for BooleanOpt {
    fn new(key: &'static str) -> Self {
        BooleanOpt{
            key: key.to_string(),
            value: false,
        }
    }
    fn describe(&self) {

    }
    fn add_argument(&self, value: String) {

    }
    fn update_value(&self, value: bool) {

    }
}

pub struct KeywordOpt {
    key: String,
    value: String,
}
impl Option<String> for KeywordOpt {
    fn new(key: &'static str) -> KeywordOpt { 
        KeywordOpt{
            key: key.to_string(),
            value: "".to_string(),
        }
    }
    fn describe(&self) {

    }
    fn add_argument(&self, value: String) {

    }
    fn update_value(&self, value: String) {

    }
}

pub struct NumericOpt {
    key: String,
    value: i32,
}
impl Option<i32> for NumericOpt {
    fn new(key: &'static str) -> NumericOpt { 
        NumericOpt{
            key: key.to_string(),
            value: 0,
        }
    }
    fn describe(&self) {

    }
    fn add_argument(&self, value: String) {

    }
    fn update_value(&self, value: i32) {

    }
}
