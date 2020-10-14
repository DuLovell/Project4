document.addEventListener('DOMContentLoaded', function() {
	
	const posts = document.querySelectorAll(".heart");
	for (let i = 0; i < posts.length; i++ ) {
		posts[i].onclick = function() {
			count_like(posts[i].parentNode);
		}
	}

	load_index();

	




})

function count_like(post) {
	console.log(post);
}

function create_post() {
	const content = document.querySelector("#new-post-content");
	fetch('/create_post', {
		method: 'POST',
		body: JSON.stringify({
			content: content.value
		})
	})
}

function load_index(request) {
	fetch('/if_authenticated', {
			method: 'GET',
		})
		.then(response => response.json())
		.then(answer => {
			console.log(answer);

			if (answer === 'True') {
				document.querySelector('#new-post').style.display = 'block';

				// Select all input fields from 'new-post' form to be used later
				const content = document.querySelector('#new-post-content');
				const submit = document.querySelector('#new-post-btn');
			
				// Disable submit button by default
				submit.disabled = true;

				// Listen for input to be typed into the input field
				content.onkeyup = () => {
					if (content.value.length > 0) {
						submit.disabled = false;
					}
					else {
						submit.disabled = true;
					}
				}

				// Listen for submission of form
				document.querySelector('#create-post').onsubmit = function() {
					create_post();
				}
			}
			else {
				document.querySelector('#new-post').style.display = 'none';
			}
		});
}