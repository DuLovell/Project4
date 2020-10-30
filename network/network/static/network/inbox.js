document.addEventListener('DOMContentLoaded', function() {
	
	const posts = document.querySelectorAll(".heart");
	for (let i = 0; i < posts.length; i++ ) {
		posts[i].onclick = function() {
			count_like(posts[i].parentNode);
		}
	}

	const posts_edit = document.querySelectorAll(".post-edit");
	for (let i = 0; i < posts_edit.length; i++ ) {
		posts_edit[i].onclick = function() {
			
			edit(posts_edit[i].parentNode);
			this.disabled = false;
		}
	}

	load_index();
	

})

function edit(post) {


	const username = post.children[0].children[0].innerHTML;
	var post_text = post.children[1].innerHTML;
	var content = post.children[1];
	const created_date = post.children[0].children[1].innerHTML;

	content.innerHTML = `<textarea id="edit-area">${ content.innerHTML }</textarea>
	<button style="position: absolute; margin: 24px 10px;" id="edit-btn">Edit</button>`;
	document.getElementById("edit-btn").onclick = function() {
		fetch('/edit_post', {
			method: 'POST',
			body: JSON.stringify({
				username: username,
				old_content: post_text,
				new_content: document.querySelector("#edit-area").value,
				created_date: created_date
			})
		})
		.then(response => response.json())
		.then(answer => {
			content.innerHTML = answer;
		})
	}


}

function count_like(post) {
	/*console.log(post.children[3]);*/
	
	const username = post.children[0].children[0].innerHTML;
	const content = post.children[1].innerHTML;
	const created_date = post.children[0].children[1].innerHTML;

	fetch('/manage_like', {
		method: 'POST',
		body: JSON.stringify({
			username: username,
			content: content,
			created_date: created_date
		})
	})
	.then(response => response.json())
	.then(answer => {
		post.children[3].innerHTML = answer;
	})
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
						submit.style.background = "#88bed1";
					}
					else {
						submit.disabled = true;
						submit.style.background = "#ADD8E6";
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


