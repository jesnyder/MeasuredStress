class StudyRecord {
  constructor(name) {
    this._name = name;
    this._behavior = 0;
  }

  get name() {
    return this._name
  }
}

class HiRecord extends StudyRecord {
  constructor(name, vrExperience) {
    super(name);
    this._vrExperience = vrExperience;
  }
}

const rec01 = new HiRecord('rec01', 'AquaMan')
console.log(rec01)
