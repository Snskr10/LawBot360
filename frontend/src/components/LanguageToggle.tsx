import { useState } from 'react';

const languages = [
  { value: 'en', label: 'English' },
  { value: 'hi', label: 'हिंदी' },
];

export default function LanguageToggle() {
  const [selected, setSelected] = useState<string>(
    localStorage.getItem('lawbot360-lang') || 'en'
  );

  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const value = event.target.value;
    setSelected(value);
    localStorage.setItem('lawbot360-lang', value);
    // In future we can wire this to a translation/i18n provider
  };

  return (
    <select
      className="language-toggle"
      value={selected}
      onChange={handleChange}
    >
      {languages.map((language) => (
        <option key={language.value} value={language.value}>
          {language.label}
        </option>
      ))}
    </select>
  );
}

