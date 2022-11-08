// describe each participant as an object

const record = {

  recordID: 'tbd',
  _study: 'tbd', // '_' prefix used as privacy convention, not to be directly changed
  date: 'tbd',
  timeBegin: 'tbd',
  gender: 'tbd',
  vrExperience: 'tbd',
  wearable: 'tbd',
  acc: 'tbd',
  bvp: 'tbd',
  hr: 'tbd',
  eda: 'tbd',
  temp: 'tbd',

  checkRecord() {
  console.log('RecordID = ' + this.recordID)
  },
  // retrieve study and recordID
  get checkStudy() {
    if (this._study && typeof(this.recordID) != 'number') {
      return ('_study/recordID  ' + this._study + '/' + this.recordID )
    } else {
      return('Missing _study or recordID')
    }
  },
  // set the gender
  set setGender(gender) {
    if (typeof gender != 'number') {
      record.gender = gender;
      return(record.gender)
    } else {
      console.log('You cannot assign a number to a gender.')
    }
    }

}

record.checkRecord()
record._study = 'HI'
console.log('Study = ' + record._study)
console.log(record.checkStudy)
record.setGender = 'Male'
console.log(record.gender)
console.log(record)
