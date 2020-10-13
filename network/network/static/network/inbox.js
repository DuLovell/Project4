document.addEventListener('DOMContentLoaded', function() {
	
	const posts = document.getElementsByClassName("heart")
	for (let i = 0; i < posts.length; i++ ) {
		posts[i].addEventListener('click', count_like());
	}
})

function count_like() {
	pass
}