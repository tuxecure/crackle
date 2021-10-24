
// Entry point for crackle
// Will be used to figure out what the user wants, by reading the command line

mod options;

fn main() {
    println!("Welcome to Crackle!");
    //let mut config = std::collections::HashSet::<Option<Any>>::new();

    let verbosity = options::NumericOpt::new("verbosity")
        .update_value(0)
        .add_argument("--verbose")
        .add_argument("-v");
    let dryness = options::BooleanOpt::new("dryness")
        .update_value(false)
        .add_argument("--verbose")
        .add_argument("-v");
    let dryness = options::KeywordOpt::new("basepath")
        .update_value(false)
        .add_argument("--basepath")
        .add_argument("-v");

    help();
}

fn help() {
}
