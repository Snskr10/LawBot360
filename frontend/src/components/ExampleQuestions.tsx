import React from 'react';
import './ExampleQuestions.css';

type ExampleQuestionsProps = {
  questions: string[];
  onQuestionClick: (question: string) => void;
};

const ExampleQuestions: React.FC<ExampleQuestionsProps> = ({ questions, onQuestionClick }) => {
  return (
    <div className="example-questions">
      <div className="example-questions-header">
        <span className="example-questions-icon">⚡</span>
        <h3 className="example-questions-title">Examples of questions you can ask me:</h3>
      </div>
      <div className="example-questions-grid">
        {questions.map((question, index) => (
          <button
            key={index}
            className="example-question-card"
            onClick={() => onQuestionClick(question)}
          >
            {question}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ExampleQuestions;

