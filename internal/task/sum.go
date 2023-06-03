package task

import (
	"context"
	"encoding/json"
	"log"

	"github.com/hibiken/asynq"
)

const (
	TypeExampleSum = "example:sum"
)

type ExampleSumPayload struct {
	Number1 int
	Number2 int
}

func NewExampleSumPayload(number1, number2 int) (*asynq.Task, error) {
	payload, err := json.Marshal(ExampleSumPayload{number1, number2})
	if err != nil {
		return nil, err
	}
	return asynq.NewTask(TypeExampleSum, payload), nil
}

type SumProcessor struct{}

func NewSumProcessor() *SumProcessor {
	return &SumProcessor{}
}

func (p *SumProcessor) ProcessTask(ctx context.Context, t *asynq.Task) error {
	var payload ExampleSumPayload
	if err := json.Unmarshal(t.Payload(), &payload); err != nil {
		return err
	}
	sum := payload.Number1 + payload.Number2
	log.Printf("%d+%d=%d\n", payload.Number1, payload.Number2, sum)
	return nil
}
