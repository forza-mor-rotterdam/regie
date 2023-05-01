import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    static values = {
        queryString: String
    }

    connect() {
        console.log("queryStringValue", this.queryStringValue)
        const inputList = document.getElementsByTagName("input")
        for (let i=0; i<inputList.length; i++){
            inputList[i].addEventListener('change', this.onInputChange)
        }
    }

    onInputChange(e) {
        console.log("onInputChange", e)
        document.getElementById('filterForm').requestSubmit()
    }

    onToggleShow(e) {
        e.target.closest("div").classList.toggle("show")
    }
}
