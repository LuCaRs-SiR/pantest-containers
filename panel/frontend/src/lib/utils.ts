export function clsx(...classes: (string | false | null | undefined)[]) {
	return classes.filter(Boolean).join(' ');
}

export function formatDate(value: string | number | Date) {
	return new Date(value).toLocaleString('pl-PL');
}
