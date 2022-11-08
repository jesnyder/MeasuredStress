class eachRecord {
  constructor(name, study) {
    this._name = name;
    this._study = study;
  }

  get name() {
    return this._name;
  }
}

for (i=0; i<10; i++) {
  let recName = 'rec' + (i.toString())
  console.log('recName = ' + recName)

  // creates a new instance of the class
  let recNameNew = new eachRecord(recName, i)
  console.log(recNameNew.name)
  console.log(recNameNew)

}
