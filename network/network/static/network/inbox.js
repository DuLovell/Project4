document.addEventListener('DOMContentLoaded', function() {
	
	const posts = document.querySelectorAll(".heart");
	for (let i = 0; i < posts.length; i++ ) {
		posts[i].onclick = function() {
			count_like(posts[i].parentNode);
		}
	}



	document.querySelector('#create-post').onsubmit = function() {
		create_post();
	}

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