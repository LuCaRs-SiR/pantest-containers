/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				'cockpit-bg': '#0A0A0F',
				'cockpit-panel': '#111118',
				'cockpit-accent': '#00AFFF',
				'cockpit-danger': '#FF0055',
				'cockpit-text': '#EAEAEA',
				'cockpit-muted': '#9A9A9A',
				'cockpit-terminal': '#000000',
				'cockpit-terminal-green': '#00FF7F'
			}
		}
	},
	plugins: []
};
