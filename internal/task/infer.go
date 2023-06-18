package task

import (
	"context"
	"fmt"
	"log"

	"golang.org/x/exp/slices"

	"github.com/hibiken/asynq"

	"github.com/m-nny/ninetails/internal/utils"
	triton "github.com/m-nny/ninetails/proto/triton/client"
)

const (
	TypeInferCifar = "infer:cifar"
)

type InferCifarPayload []byte

func NewInferCifarPayload(img []byte) (*asynq.Task, error) {
	payload := img
	return asynq.NewTask(TypeInferCifar, payload), nil
}

func parseInferCifarPayload(t *asynq.Task) (InferCifarPayload, error) {
	payload := t.Payload()
	return payload, nil
}

type InferCifarProcessor struct {
	tritonClient triton.GRPCInferenceServiceClient
}

func NewInferCifarProcessor(tritonClient triton.GRPCInferenceServiceClient) *InferCifarProcessor {
	return &InferCifarProcessor{tritonClient: tritonClient}
}

func (p *InferCifarProcessor) ProcessTask(ctx context.Context, t *asynq.Task) error {
	payload, err := parseInferCifarPayload(t)
	if err != nil {
		return err
	}
	log.Printf("img(%d)\n", len(payload))
	if err := p.infer(ctx, payload); err != nil {
		log.Printf("error during infer(): %v\n", err)
		return err
	}
	return nil
}

func (p *InferCifarProcessor) infer(ctx context.Context, img []byte) error {
	modelName := "cifar_ensemble"
	inferInputs := []*triton.ModelInferRequest_InferInputTensor{
		{
			Name:     "image_jpg",
			Datatype: "UINT8",
			Shape:    []int64{1, int64(len(img))},
		},
	}
	// Create inference request for specific model/version
	modelInferRequest := triton.ModelInferRequest{
		ModelName: modelName,
		Inputs:    inferInputs,
	}

	modelInferRequest.RawInputContents = append(modelInferRequest.RawInputContents, img)

	// Submit inference request to server
	modelInferResponse, err := p.tritonClient.ModelInfer(ctx, &modelInferRequest)
	if err != nil {
		log.Printf("Error processing InferRequest: %v", err)
		return err
	}
	log.Printf("response: %s\v", modelInferResponse)
	idx, prob, err := postprocess(modelInferResponse)
	if err != nil {
		return err
	}
	log.Printf("idx: %d prob: %f\n", idx, prob)
	return nil
}

func postprocess(res *triton.ModelInferResponse) (int, float32, error) {
	logits, err := getFloat32Output(res, "logits")
	if err != nil {
		log.Printf("error getting output: %v\n", err)
		return 0, 0, err
	}
	probs, err := getFloat32Output(res, "probs")
	if err != nil {
		log.Printf("error getting output: %v\n", err)
		return 0, 0, err
	}
	class := argmax(logits)
	return class, probs[class], nil
}

func getFloat32Output(res *triton.ModelInferResponse, name string) ([]float32, error) {
	idx := slices.IndexFunc(res.GetOutputs(), func(output *triton.ModelInferResponse_InferOutputTensor) bool {
		return output.Name == name
	})
	if idx == -1 {
		return nil, fmt.Errorf("output %s not found", name)
	}
	size := res.GetOutputs()[idx].Shape[1]
	return utils.ReadFloat32Slice(res.RawOutputContents[idx], int(size))
}

func argmax(arr []float32) (idx int) {
	if len(arr) == 0 {
		return -1
	}
	for i := range arr {
		if arr[idx] < arr[i] {
			idx = i
		}
	}
	return idx
}
