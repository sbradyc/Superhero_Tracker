// don't allow submission if no power is selected
function handleSubmit(event) {
    event.preventDefault()

    const form = document.getElementById('person-form')
    const inputs = [...document.getElementById('available-power-list').childNodes].filter(child => child.nodeName === 'INPUT')
    const checkedInputs = inputs.filter((input) => input.checked)

    if (checkedInputs.length === 0) {
        alert('Please select at least one power.')
    } else {
        form.submit()
    }
}