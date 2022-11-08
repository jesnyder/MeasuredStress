const recordFactory = (study, recordID) => {
  return {
    study : study,
    recordID,
    beep () {
      console.log('Beep Boop');
    }
  }
}

const rec = recordFactory('P-500', true)
rec.beep()
rec.newParameter = '100'
console.log(rec.newParameter)
console.log(rec)

const recKeys = Object.keys(rec)
console.log(recKeys)

const recEntries = Object.entries(rec)
console.log(recEntries)

const newRec = Object.assign({inflections: 100, emotion: 'Dread'})
console.log(newRec)
