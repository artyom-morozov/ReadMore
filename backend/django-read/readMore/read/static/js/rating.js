function onStarHover(star) {
	let id = parseInt(star.id[star.id.length - 1]);
	console.log('Moseover ' + id);
	for (let i = 0; i <= id - 1; i++) {
		document.getElementById(`star${i + 1}`).classList.add('star-active');
	}
}
function onStarMove(star) {
	let id = parseInt(star.id[star.id.length - 1]);
	console.log('move ' + id);
	for (let i = 0; i <= id - 1; i++) {
		document.getElementById(`star${i + 1}`).classList.remove('star-active');
	}
}

function onStarClick(star) {
	let star_val = parseInt(star.id[star.id.length - 1]);
	let tokens = location.pathname.split('/');
	let book_id = tokens[tokens.length - 1];
	let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	console.log(`A `);
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/add-rating/', true);
	// xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.setRequestHeader('X-CSRFToken', csrftoken);
	xhr.send({
		book_id: book_id,
		value: star_val
	});
}
