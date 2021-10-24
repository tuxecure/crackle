
// Entry point for crackle
// Will be used to figure out what the user wants, by reading the command line

mod options;
use options::Config;

fn main() {
    println!("Welcome to Crackle!");
    //let mut config = std::collections::HashSet::<Option<Any>>::new();

    let verbosity = options::NumericParameter::new("verbosity")
        .update_value(0)
        .add_argument("--verbose")
        .add_argument("-v");
    let dryness = options::Lever::new("dryness")
        .update_value(false)
        .add_argument("--verbose")
        .add_argument("-v");
    let dryness = options::TextParameter::new("basepath")
        .update_value(".".to_string())
        .add_argument("--basepath")
        .add_argument("-v");

    help();
}

fn help() {
}
