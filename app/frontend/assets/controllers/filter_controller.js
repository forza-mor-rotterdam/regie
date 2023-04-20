import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    connect() {
        const inputList = document.getElementsByTagName("input")
        for (let i=0; i<inputList.length; i++){
            inputList[i].addEventListener('change', this.onInputChange)
        }
    }

    onInputChange() {
        document.getElementById('filterForm').requestSubmit()
    }

    onToggleShow(e) {
        e.target.closest("div").classList.toggle("show")
    }
}
