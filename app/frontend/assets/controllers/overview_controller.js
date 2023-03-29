import { Controller } from '@hotwired/stimulus';

export default class extends Controller {

    connect() {
        console.log('overview_controller connected')
    }

    sortTable(e) {
        console.log(e.params)
        const frame = document.getElementById('overview');
        const url = `${frame.dataset.src}?ordering=${e.params.sort}`
        frame.setAttribute('src', url);

    }
}
