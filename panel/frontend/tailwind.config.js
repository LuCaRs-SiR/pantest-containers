/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			colors: {
				'cockpit-bg': '#0A0A0F',
				'cockpit-panel': '#111118',
				'cockpit-panel-light': '#1A1A24',
				'cockpit-accent': '#00AFFF',
				'cockpit-accent-glow': 'rgba(0, 175, 255, 0.4)',
				'cockpit-pink': '#FF00A0',
				'cockpit-pink-glow': 'rgba(255, 0, 160, 0.4)',
				'cockpit-danger': '#FF0055',
				'cockpit-text': '#EAEAEA',
				'cockpit-muted': '#9A9A9A',
				'cockpit-terminal': '#000000',
				'cockpit-terminal-green': '#00FF7F'
			},
			boxShadow: {
				'glow-accent': '0 0 12px rgba(0, 175, 255, 0.5)',
				'glow-pink': '0 0 12px rgba(255, 0, 160, 0.5)',
				'glow-green': '0 0 12px rgba(0, 255, 127, 0.4)'
			}
		}
	},
	plugins: []
};
