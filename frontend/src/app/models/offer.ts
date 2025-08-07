export interface Offer {
    id: number,
    site: string;
    url: string;
    title: string;
    company: string;
    location: string;
    experience: string;
    salary: string;
    datePosted: Date;
    validThrough: Date;
    skills: string[];
}